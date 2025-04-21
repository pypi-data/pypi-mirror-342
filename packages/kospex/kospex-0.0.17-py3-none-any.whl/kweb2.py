#!/usr/bin/env python3
""" This is the local development web server to view the Kospex database. """
from os.path import basename
import sys
import base64
from statistics import mean, median, mode, stdev, quantiles
from collections import Counter, OrderedDict
from typing import Optional, Dict, Any, List, Union

from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from kospex_bitbucket import KospexBitbucket
from kospex_query import KospexQuery
import kospex_web as KospexWeb
import kospex_utils as KospexUtils

app = FastAPI(title="Kospex Web", description="Web interface for Kospex database")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Mount static files
#app.mount("/static", StaticFiles(directory="static"), name="static")

# Helper function to convert route parameters to context dict for templates
def get_template_context(request: Request, **kwargs) -> Dict[str, Any]:
    context = {"request": request}  # FastAPI requires passing request to templates
    context.update(kwargs)
    return context

@app.get("/", response_class=HTMLResponse)
@app.get("/summary/", response_class=HTMLResponse)
@app.get("/summary/{id}", response_class=HTMLResponse)
async def summary(request: Request, id: Optional[str] = None):
    """ Serve up the summary home page """
    params = KospexWeb.get_id_params(id)
    devs = KospexQuery().developers(**params)

    dev_stats = KospexUtils.count_key_occurrences(devs, "status")
    dev_percentages = KospexUtils.convert_to_percentage(dev_stats)

    total = sum(dev_stats.values())
    dev_stats["total"] = total

    result = {}
    for name, percentage in dev_percentages.items():
        if percentage:
            dev_stats[f"{name}_percentage"] = round(percentage)
        result[name] = round(100 * (percentage / 100)) + 40

    repos = KospexQuery().repos(**params)
    repo_stats = KospexUtils.count_key_occurrences(repos, "status")

    repo_sizes = {}
    repo_percentages = KospexUtils.convert_to_percentage(repo_stats)
    # Do the total after percentages are calculated
    total = sum(repo_stats.values())
    repo_stats["total"] = total

    for name, percentage in repo_percentages.items():
        if percentage:
            repo_stats[f"{name}_percentage"] = round(percentage)
        repo_sizes[name] = round(100 * (percentage / 100)) + 40

    return templates.TemplateResponse("summary.html", 
                                     get_template_context(request, 
                                                         developers=dev_stats,
                                                         data_size=result, 
                                                         repos=repo_stats, 
                                                         repo_sizes=repo_sizes,
                                                         id=params))

@app.get("/help", response_class=HTMLResponse)
@app.get("/help/", response_class=HTMLResponse)
@app.get("/help/{id}", response_class=HTMLResponse)
async def help(request: Request, id: Optional[str] = None):
    """ Serve up the help pages """
    page = "404"
    if id:
        # Check that the id is safe to use
        valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-')
        if set(id).issubset(valid_chars):
            print("looks legit")
            page = f"help/{id}"
        else:
            page = "404"
    else:
        page = "help/index"

    try:
        return templates.TemplateResponse(f'{page}.html', get_template_context(request))
    except Exception:
        return templates.TemplateResponse('404.html', get_template_context(request), status_code=404)

@app.get("/developers/active/{repo_id}", response_class=HTMLResponse)
async def active_developers(request: Request, repo_id: str):
    """ Developer info page. """
    data = KospexQuery().summary(days=90, repo_id=repo_id)
    results = KospexQuery().active_devs_by_repo(repo_id)
    print(results)
    return templates.TemplateResponse('developers.html', 
                                     get_template_context(request, data=data, authors=results))

@app.get("/developer", response_class=HTMLResponse)
@app.get("/developer/", response_class=HTMLResponse)
@app.get("/developer/{id}", response_class=HTMLResponse)
async def dev(request: Request, id: Optional[str] = None, author_email: Optional[str] = None):
    """
    View a developers details
    """
    # WIP - migrating singled developer out of /developers/ route

    if id:
        author_email = KospexUtils.decode_base64(id)

    print(author_email)
    # Github uses +, which get interpreted as a " " in the URL.
    if author_email:
        author_email = author_email.replace(" ", "+")
    repo_list = KospexQuery().repos_by_author(author_email)
    techs = KospexQuery().author_tech(author_email=author_email)
    labels = []
    datapoints = []

    count = 0
    for tech in techs:
        labels.append(tech['_ext'])
        datapoints.append(tech['commits'])
        count += 1
        if count > 10:
            break

    return templates.TemplateResponse('developer_view.html', 
                                     get_template_context(request,
                                                         repos=repo_list,
                                                         tech=techs, 
                                                         author_email=author_email,
                                                         labels=labels, 
                                                         datapoints=datapoints))

@app.get("/tenure/", response_class=HTMLResponse)
@app.get("/tenure/{id}", response_class=HTMLResponse)
async def tenure(request: Request, id: Optional[str] = None):
    """
    View developer tenure in for all, a server, org or a repo
    """
    params = KospexWeb.get_id_params(id)
    developers = KospexQuery().developers(**params)
    active_devs = []

    for entry in developers:
        entry['tenure_status'] = KospexUtils.get_status(entry['tenure'])

    for dev in developers:
        if "Active" == dev.get("status"):
            active_devs.append(dev)

    data = {}
    data['developers'] = len(developers)
    data['active_devs'] = len(active_devs)
    days_values = [entry['tenure'] for entry in developers]

    commit_stats = KospexQuery().get_activity_stats(params)
    print(commit_stats)
    data['days_active'] = commit_stats.get('days_active')
    data['years_active'] = commit_stats.get('years_active')
    data['repos'] = commit_stats.get('repos')
    data['commits'] = commit_stats.get('commits')

    data['max'] = round(max(days_values))
    data['mean'] = round(mean(days_values), 2)
    data['mode'] = round(mode(days_values), 2)
    data['median'] = round(median(days_values), 2)
    data['std_dev'] = round(stdev(days_values), 2)

    distribution = KospexUtils.get_status_distribution(developers)
    active_d = KospexUtils.get_status_distribution(active_devs)

    return templates.TemplateResponse('tenure.html', 
                                     get_template_context(request,
                                                         data=data,
                                                         distribution=distribution, 
                                                         developers=developers, 
                                                         active_distribution=active_d))

@app.get("/developers/", response_class=HTMLResponse)
async def developers(
    request: Request, 
    author_email: Optional[str] = None,
    download: Optional[str] = None,
    days: Optional[int] = None,
    org_key: Optional[str] = None
):
    """ Developer info page. """
    devs = KospexQuery().authors(days=days, org_key=org_key)

    if author_email:
        print(author_email)
        # Github uses +, which get interpreted as a " " in the URL.
        author_email = author_email.replace(" ", "+")
        repo_list = KospexQuery().repos_by_author(author_email)
        techs = KospexQuery().author_tech(author_email=author_email)
        labels = []
        datapoints = []

        github_handle = KospexUtils.extract_github_username(author_email)

        count = 0
        for tech in techs:
            labels.append(tech['_ext'])
            datapoints.append(tech['commits'])
            count += 1
            if count > 10:
                break

        return templates.TemplateResponse('developer_view.html', 
                                         get_template_context(request,
                                                             repos=repo_list,
                                                             tech=techs, 
                                                             author_email=author_email,
                                                             labels=labels, 
                                                             github_handle=github_handle,
                                                             datapoints=datapoints))

    elif download:
        return KospexWeb.download_csv(devs)
    else:
        data = KospexQuery().summary(days=days)
        return templates.TemplateResponse('developers.html', 
                                         get_template_context(request, authors=devs, data=data))

@app.get("/landscape", response_class=HTMLResponse)
@app.get("/landscape/", response_class=HTMLResponse)
@app.get("/landscape/{id}", response_class=HTMLResponse)
async def landscape(request: Request, id: Optional[str] = None):
    """ Serve up the technology landscape metadata """
    kospex = KospexQuery()

    params = KospexWeb.get_id_params(id)
    repo_id = request.query_params.get('repo_id') or params.get("repo_id")
    org_key = request.query_params.get('org_key') or params.get("org_key")
    data = kospex.tech_landscape(org_key=org_key,repo_id=repo_id)

    download = request.query_params.get('download')

    if download:
        # TODO - need to pass in the query params for orgs or repo
        return FileResponse(KospexWeb.download_csv(data), filename="kospex_tech_landscape.csv")
    else:
        return templates.TemplateResponse('landscape.html', get_template_context(request, data=data, org_key=org_key, id=id))

@app.get("/files/repo/", response_class=HTMLResponse)
@app.get("/files/repo/{repo_id}", response_class=HTMLResponse)
async def repo_files(request: Request, repo_id: Optional[str] = None):
    """
    Show file metadata for a repo_id.
    """
    #data = KospexQuery().summary(days=90,repo_id=repo_id)
    #results = KospexQuery().active_devs_by_repo(repo_id)
    #print(results)
    data = None
    if repo_id:
        data = KospexQuery().repo_files(repo_id=repo_id)
    return templates.TemplateResponse('files.html', get_template_context(request, data=data))

@app.get("/repos", response_class=HTMLResponse)
@app.get("/repos/", response_class=HTMLResponse)
@app.get("/repos/{id}", response_class=HTMLResponse)
async def repos(request: Request, id: Optional[str] = None):
    """ display repo information. """

    params = KospexWeb.get_id_params(id)
    print(params)
    repo_id = request.query_params.get('repo_id') or params.get("repo_id")
    org_key = request.query_params.get('org_key') or params.get("org_key")
    server = request.query_params.get('server') or params.get("server")

    kospex = KospexQuery()

    page = {}
    # TODO - validate params
    techs = None
    # Maintenance ranges
    ranges = None

    page['repo_id'] = repo_id

    data = []

    if org_key:
        parts = org_key.split("~")
        if len(parts) == 2:
            page['git_server'] = parts[0]
            page['git_owner'] = parts[1]
            techs = kospex.tech_landscape(org_key=org_key)
            ranges = kospex.commit_ranges2(org_key=org_key)
            print(kospex.commit_ranges2(repo_id=repo_id,org_key=org_key))
    elif server:
        page['git_server'] = server

    # The repos method handles null values for parameters
    data = kospex.repos(org_key=org_key,server=server)
    active_devs = kospex.active_devs()
    for row in data:
        row['active_devs'] = active_devs.get(row['_repo_id'],0)

    developers = kospex.developers(org_key=org_key,server=server)
    developer_status = KospexUtils.repo_stats(developers,"last_commit")

    return templates.TemplateResponse('repos.html', get_template_context(request, data=data,
        page=page, ranges=ranges, techs=techs, developer_status=developer_status))

@app.get("/servers/", response_class=HTMLResponse)
async def servers(request: Request):
    """ display Git server information. """

    kquery = KospexQuery()
    data = kquery.server_summary()
    print(data)

    return templates.TemplateResponse('servers.html', get_template_context(request, data=data))

@app.get("/observations/", response_class=HTMLResponse)
async def observations(request: Request):
    """ display observation information. """
    kquery = KospexQuery()
    repo_id = request.query_params.get('repo_id')
    observation_key = request.query_params.get('observation_key')

    if observation_key:
        # We should have an observation key and a repo_id for this to work
        print("observation_key",observation_key)
        return templates.TemplateResponse('observations_repo_key.html',
                               get_template_context(request,
                                                   data=kquery.observations_summary(repo_id=repo_id,observation_key=observation_key),
                                                   observation_key=observation_key,repo_id=repo_id))

    elif repo_id:
        print("repo_id",repo_id)

        return templates.TemplateResponse('observations_repo.html',
                               get_template_context(request,
                                                   data=kquery.observations_summary(repo_id=repo_id),
                                                   repo_id=repo_id))
    else:
        return templates.TemplateResponse('observations.html', get_template_context(request, data=kquery.observations_summary()))

@app.get("/orgs/", response_class=HTMLResponse)
async def orgs(request: Request):
    """ display repo information. """

    org = request.query_params.get('org')

    kospex = KospexQuery()

    git_orgs = kospex.orgs()
    active_devs = kospex.active_devs(org=True)
    print(active_developers)

    for row in git_orgs:
        row['active_devs'] = active_devs.get(row['org_key'],0)

    return templates.TemplateResponse('orgs.html', get_template_context(request, data=git_orgs))

@app.get("/repo/{repo_id}", response_class=HTMLResponse)
async def repo(request: Request, repo_id: str):
    """ display repo information. """
    kospex = KospexQuery()
    #data = kospex.repos()
    commit_ranges = kospex.commit_ranges(repo_id)
    print(commit_ranges)
    email_domains = kospex.email_domains(repo_id=repo_id)
    #summary = kospex.author_summary(repo_id)
    summary=kospex.author_summary(repo_id)
    techs = kospex.tech_landscape(repo_id=repo_id)

    developers = kospex.developers(repo_id=repo_id)
    developer_status = KospexUtils.repo_stats(developers,"last_commit")

    # TODO - make generic function for radar graph (in developer view too)
    labels = []
    datapoints = []
    count = 0
    for tech in techs:
        labels.append(tech['Language'])
        datapoints.append(tech['count'])
        count += 1
        if count > 10:
            break

    return templates.TemplateResponse('repo_view.html',
                           get_template_context(request,
                           repo_id=repo_id,
                           ranges=commit_ranges,
                           email_domains=email_domains,
                           landscape = techs,
                           developer_status=developer_status,
                           labels=labels,datapoints=datapoints,
                           summary=summary))

@app.get("/tech/{tech}", response_class=HTMLResponse)
async def repo_with_tech(request: Request, tech: str):
    """ Show repos with the given tech. """
    #print(tech)
    repo_id = request.query_params.get('repo_id')
    kospex = KospexQuery()
    template = "repos.html"
    if repo_id:
        repos_with_tech = kospex.repo_files(tech,repo_id=repo_id)
        template = "repo_files.html"
    else:
        repos_with_tech = kospex.repos_with_tech(tech)

    return templates.TemplateResponse(template, get_template_context(request, data=repos_with_tech, page = {}))

@app.get("/commits/", response_class=HTMLResponse)
async def commits(request: Request):
    """ display Git commits information. """
    repo_id = request.query_params.get('repo_id',"")
    author_email = request.query_params.get('author_email')
    commiter_email = request.query_params.get('committer_email')
    print(author_email)
    data = KospexQuery().commits(limit=100,repo_id=repo_id,
                                 author_email=author_email, committer_email=commiter_email)
    return templates.TemplateResponse('commits.html', get_template_context(request, commits=data, repo_id=repo_id))

@app.get("/hotspots/{repo_id}", response_class=HTMLResponse)
async def hotspots(request: Request, repo_id: str):
    """ display Git commits information. """
    data = KospexQuery().hotspots(repo_id=repo_id)
    return templates.TemplateResponse('hotspots.html', get_template_context(request, data=data))

@app.get("/meta/author-domains", response_class=HTMLResponse)
async def author_domains(request: Request):
    """ display repo information. """
    kospex = KospexQuery()
    email_domains = kospex.email_domains()
    return templates.TemplateResponse('meta-author-domains.html', get_template_context(request, email_domains=email_domains))

# Error Handling Routes
@app.exception_handler(404)
async def page_not_found(request: Request, exc: HTTPException):
    """ Serve up the 404 page """
    return templates.TemplateResponse('404.html', get_template_context(request), status_code=404)

# Experimental and Development Routes
@app.get("/bootstrap/", response_class=HTMLResponse)
async def bootstrap(request: Request):
    """ bootstrap 5 dev playground. """
    return templates.TemplateResponse('bootstrap5.html', get_template_context(request))

@app.get("/tech-change/", response_class=HTMLResponse)
async def tech_change(request: Request):
    """ Radars for tech change. """
    labels = [ "Java", "Go", "JavaScript", "Python", "Kotlin" ]
    return templates.TemplateResponse('tech-change.html', get_template_context(request, labels=labels))

@app.get("/metadata/", response_class=HTMLResponse)
async def metadata(request: Request):
    """ Metadata about the kospex DB and repos. """
    data = KospexQuery().summary()
    return templates.TemplateResponse('metadata.html', get_template_context(request, **data))

@app.get("/osi/", response_class=HTMLResponse)
@app.get("/osi/{id}", response_class=HTMLResponse)
async def osi(request: Request, id: Optional[str] = None):
    """
    Functions around an Open Source Inventory
    """
    params = KospexWeb.get_id_params(id)
    deps = KospexQuery().get_dependency_files(id=params)
    for file in deps:
        file["days_ago"] = KospexUtils.days_ago(file.get("committer_when"))
        file["status"] = KospexUtils.development_status(file.get("days_ago"))
    file_number = len(deps)
    status = KospexUtils.repo_stats(deps,"committer_when")
    print(status)

    return templates.TemplateResponse('osi.html', get_template_context(request, data=deps, file_number=file_number, status=status))

@app.get("/dependencies/", response_class=HTMLResponse)
@app.get("/dependencies/{id}", response_class=HTMLResponse)
async def dependencies(request: Request, id: Optional[str] = None):
    """
    Display SCA information
    """
    params = KospexWeb.get_id_params(id)

    data = KospexQuery().get_dependencies(id=params)
    print(data)

    return templates.TemplateResponse('dependencies.html', get_template_context(request, data=data))

@app.get("/orphans/", response_class=HTMLResponse)
@app.get("/orphans/{id}", response_class=HTMLResponse)
async def orphans(request: Request, id: Optional[str] = None):
    """
    Display orphan information
    """
    params = KospexWeb.get_id_params(id)

    data = KospexQuery().get_orphans(id=params)

    return templates.TemplateResponse('orphans.html', get_template_context(request, data=data))

@app.get("/bubble/{id}", response_class=HTMLResponse)
@app.get("/bubble/{id}/{template}", response_class=HTMLResponse)
async def bubble(request: Request, id: str, template: Optional[str] = "bubble"):
    """
    Display a bubble or treemap chart of developers in a repo
    or the repos for an org_key
    or the repos for a given user

    Show the developers for a repo_id
    /bubble/<repo_id>

    Show the developers for an org_key
    /bubble/<org_key>

    Show the developers for a git_server
    /bubble/<git_server>

    Show repos for a developer with a base64 encoded email
    /bubble/EMAIL_B64

    Show repo view of an org_key
    /bubble/repo/<org_key>

    """

    link_url = ""

    if KospexUtils.parse_repo_id(id):
        link_url = f"repo/{id}"
    elif KospexUtils.is_base64(id):
        link_url = f"dev/{id}"
    else:
        link_url = f"{id}"

    #if "~" in repo_id:
    #    link_url = f"repo/{repo_id}"
    #else:
    #    print("maybe a dev?")
    #    link_url = f"dev/{repo_id}"
    html_template = f"{template}.html"

    return templates.TemplateResponse(html_template, get_template_context(request, link_url=link_url,
        template=template, id=id))

    #return render_template('bubble.html',link_url=link_url)
    #return render_template('treemap.html',link_url=link_url)

# This was a spike to break out the graph work and make it less clunky
# @app.route('/graph-api/<id>')
# def graph_api(id):

#     org_info = []
#     data = {
#             "nodes": [],
#             "links": []
#     }
#     links = []
#     nodes = []

#     if KospexUtils.parse_org_key(id):
#         org_info = KospexQuery().get_graph_info(org_key=id)

#     elif KospexUtils.parse_repo_id(id):
#         org_info = KospexQuery().get_graph_info(repo_id=id)

#     elif KospexUtils.is_base64(id):
#         email = KospexUtils.decode_base64(id)
#         org_info = KospexQuery().get_graph_info(author_email=email,
#             by_repo=True)

#     elif focus:

#         if focus == "repo":
#             org_info = KospexQuery().get_graph_info(repo_id=repo_id)
#         else:
#             org_info = KospexQuery().get_graph_info(author_email=author_email,
#                 by_repo=True)
#             print("Unknown focus")
#             print(org_info)

#         print(f"in focus, with focus: {focus}")

#     elif repo_id:
#         org_info = KospexQuery().get_repo_files_graph_info(repo_id=repo_id)
#         #org_info = KospexQuery().get_graph_info(org_key=org_key)

#     elif author_email:
#         # This should be the b64 parameter that's decoded
#         org_info = KospexQuery().get_graph_info(author_email=author_email)

#     elif git_server:
#         org_info = KospexQuery().get_graph_info(git_server=git_server)

#     data["nodes"] = nodes
#     data["links"] = links

#     return data

@app.get("/graph", response_class=HTMLResponse)
@app.get("/graph/", response_class=HTMLResponse)
@app.get("/graph/{org_key}", response_class=HTMLResponse)
async def graph(request: Request, org_key: Optional[str] = None):
    """
    Force directed graphs for data in the Kospex DB.
    """
    author_email = request.query_params.get('author_email')
    if author_email:
        # This is a weird old skool http thing
        # where spaces were represented by + signs
        author_email = author_email.replace(" ","+")
    repo_id = request.query_params.get('repo_id')

    if repo_id:
        org_key = f"?repo_id={repo_id}"
    elif author_email:
        org_key = f"?author_email={author_email}"

    return templates.TemplateResponse('graph.html', get_template_context(request, org_key=org_key))

@app.get("/org-graph", response_class=HTMLResponse)
@app.get("/org-graph/", response_class=HTMLResponse)
@app.get("/org-graph/{org_key}", response_class=HTMLResponse)
@app.get("/org-graph/{focus}/{org_key}", response_class=HTMLResponse)
async def org_graph(request: Request, focus: Optional[str] = None, org_key: Optional[str] = None):
    """
    Return JSON data for the force directed graph.

    """
    ### MVP

    params = KospexWeb.get_id_params(org_key)
    repo_id = request.query_params.get('repo_id') or params.get("repo_id")
    org_key = request.query_params.get('org_key') or params.get("org_key")
    git_server = request.query_params.get('server') or params.get("server")

    #repo_id = request.args.get('repo_id')
    author_email = None
    #git_server = None
    # TODO we're hacking around if we're actualy passed a repo_id and not an org_key

    if org_key:
        repo_parts = KospexUtils.parse_repo_id(org_key)
        if repo_parts:
            repo_id = org_key
            org_key = None
        elif KospexUtils.parse_org_key(org_key):
            print(f"looks like {org_key} is an org_key")

        elif KospexUtils.is_base64(org_key):
            # Doesn't look like an org_key
            # Possibly an author email
            base64_bytes = org_key.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            decoded = message_bytes.decode('ascii')
            # Rough check to see if it's an email
            if "@" in decoded:
                org_key = None
                author_email = decoded
        else:
            # Possibly just a git server
            git_server = org_key
            org_key = None


    print(f"org_key: {org_key}\nrepo_id: {repo_id}\nfocus: {focus}")

    org_info = []

    if org_key:
        org_info = KospexQuery().get_graph_info(org_key=org_key)

    elif focus:

        if focus == "repo":
            org_info = KospexQuery().get_graph_info(repo_id=repo_id)
        else:
            org_info = KospexQuery().get_graph_info(author_email=author_email,
                by_repo=True)
            print("Unknown focus")

        print(f"in focus, with focus: {focus}")

    elif repo_id:
        org_info = KospexQuery().get_repo_files_graph_info(repo_id=repo_id)
        #org_info = KospexQuery().get_graph_info(org_key=org_key)

    elif author_email:
        # This should be the b64 parameter that's decoded
        org_info = KospexQuery().get_graph_info(author_email=author_email)

    elif git_server:
        org_info = KospexQuery().get_graph_info(git_server=git_server)

    else:
        author_email = request.query_params.get('author_email')
        if author_email:
            author_email = author_email.replace(" ","+")
        org_info = KospexQuery().get_graph_info(author_email=author_email)

    dev_lookup = {}
    repo_lookup = {}
    file_lookup = {}
    links = []
    nodes = []

    #print(org_info)

    for element in org_info:

        last_commit = element.get("last_commit")
        status = KospexUtils.development_status(KospexUtils.days_ago(last_commit))

        group_numbers = {}
        group_numbers['Active'] = 1
        group_numbers['Aging'] = 2
        group_numbers['Stale'] = 3
        group_numbers['Unmaintained'] = 4

        group = 1
        if org_key:
            # we only have 1 group, and that's developers
            group = 1
            # in graph, group is used to link between
        else:
            group = group_numbers.get(status,4)

        b64_email = KospexUtils.encode_base64(element.get('author'))

        if element['author'] not in dev_lookup:
            dev_lookup[element['author']] = { "id": element['author'],
                                             "id_b64": b64_email,
                                             "group": group,
                                             "node_type": "developer",
                                             "label": KospexUtils.extract_github_username(element['author']),
                                             "info": element['author'],
                                             "commits": element.get("commits"),
                                             "status_group": group_numbers.get(status,4),
                                             "status": status,
                                             "last_commit": last_commit,
                                             "repos": 1 }
        else:
            dev_lookup[element['author']]['repos'] += 1


        if repo_id and not focus:
            # We're handling files not repos
            file_path = element.get('file_path')
            if element.get('file_path') not in file_lookup:
                file_lookup[element['file_path']] = { "id": element['file_path'],
                                                "group": 2,
                                                "label": basename(element['file_path']),
                                                "info": element['file_path'] }

        elif element['_repo_id'] not in repo_lookup:
            repo_lookup[element['_repo_id']] = { "id": element['_repo_id'],
                                                "group": 2,
                                                "node_type": "repo",
                                                "commits": element.get("commits",0),
                                                "status_group": group_numbers.get(status,4),
                                                "status": status,
                                                "link": f"/repo/{element.get('_repo_id')}",
                                                "last_commit": last_commit,
                                                "label": element['_git_repo'],
                                                "info": element['_repo_id'] }

        link_key = "_repo_id"
        if repo_id:
            link_key = "file_path"

        links.append({"source": element['author'],
                      "target": element.get(link_key),
                      "commits": element['commits']})

    for element in dev_lookup:
        nodes.append(dev_lookup[element])

    for element in repo_lookup:
        nodes.append(repo_lookup[element])

    for element in file_lookup:
        nodes.append(file_lookup[element])

    data = {
            "nodes": [
                { "id": "Dev1", "group": 1, "info": "Developer 1 info" },
                { "id": "Dev2", "group": 1, "info": "Developer 2 info" },
                { "id": "Repo1", "group": 2, "info": "Repository 1 info" },
                { "id": "Repo2", "group": 2, "info": "Repository 2 info" },
                { "id": "Repo3", "group": 2, "info": "Repository 3 info" }
            ],
            "links": [
                { "source": "Dev1", "target": "Repo1", "commits": 50 },
                { "source": "Dev1", "target": "Repo2", "commits": 30 },
                { "source": "Dev2", "target": "Repo1", "commits": 20 },
                { "source": "Dev2", "target": "Repo3", "commits": 40 },
                { "source": "Dev3", "target": "Repo2", "commits": 60 },
                { "source": "Dev3", "target": "Repo3", "commits": 10 }
            ]
        }

    data["nodes"] = nodes
    data["links"] = links

    return templates.TemplateResponse('graph.html', get_template_context(request, data=data))

def kweb():
    """ Run the web server. """
    all_interfaces = False
    if "-all" in sys.argv:
        all_interfaces = True
        print("Found -all")

    import uvicorn
    
    if len(sys.argv) > 1:
        if "-debug" in sys.argv:
            print("\n#\nRunning in DEBUG mode.\n#\n\n")
            if all_interfaces:
                print("WARNING: LISTENING ON 0.0.0.0\n")
                uvicorn.run("kweb2:app", host="0.0.0.0", port=8000, reload=True)
            else:
                uvicorn.run("kweb2:app", host="127.0.0.1", port=8000, reload=True)
        else:
            exit("Unknown option, try -debug.")
    else:
        print("\n#\nRunning in NON debug, local mode.\n#\n\n")
        uvicorn.run("kweb2:app", host="127.0.0.1", port=8000)

if __name__ == "__main__":
    kweb()
