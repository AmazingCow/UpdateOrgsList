#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        update.py                                 ##
##            █ █        █ █        UpdateOrgsList                            ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2017                        ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

## Imports ##
import os;
import os.path;
import urllib;
import json;
import time;


################################################################################
## Vars                                                                       ##
################################################################################
BASE_URL = "https://api.github.com/users/{ORGANIZATION_NAME}/repos"

ORGANIZATION_NAMES = [
    "AmazingCow-Game-Core",
    "AmazingCow-Game-Framework",
    "AmazingCow-Game-Tool",
    "AmazingCow-Game",
    "AmazingCow-Libs",
    "AmazingCow-Tools",
    "AmazingCow-Imidiar",
];

THIS_ORGANIZATION="AmazingCow-{0}".format(
    os.path.basename(os.path.abspath("../")).replace("-List", "")
);


################################################################################
## Functions                                                                  ##
################################################################################
def fetch_list_repos(organization_name):
    url      = BASE_URL.format(ORGANIZATION_NAME=organization_name);
    response = urllib.urlopen(url);
    data     = json.loads(response.read());


    print "Fetching repos for: ({0})".format(organization_name);
    repos = [];
    for info in data:
        repos.append({
            "name" : info["name"     ],
            "url"  : info["clone_url"]
        });

    return repos;


def build_url_for_org(org_name):
    return "https://github.com/{0}".format(org_name);

def build_bullet_item_for_repo(repo_info):
    return "* [{0}]({1})\n".format(repo_info["name"], repo_info["url"]);

def build_bullet_item_for_org(org_name):
    return "* [{0}]({1})\n".format(org_name, build_url_for_org(org_name));


################################################################################
## Script                                                                     ##
################################################################################
## Update
repos_info     = fetch_list_repos(THIS_ORGANIZATION);
template_lines = open("template.md").readlines();

readme_file = open("../README.md", "w");

for line in template_lines:
    line = line.replace("\n", "");
    if("__ORGANIZATION_NAME__" in line):
        line = line.replace("__ORGANIZATION_NAME__", THIS_ORGANIZATION);

    if("__ORGANIZATION_URL__" in line):
        line = line.replace(
            "__ORGANIZATION_URL__",
            build_url_for_org(THIS_ORGANIZATION)
        );

    if("__REPOS_LIST__" in line):
        line = "";
        for repo_info in repos_info:
            line += build_bullet_item_for_repo(repo_info);

    if("__ALL_ORGANIZATIONS__" in line):
        line = "";
        for org_name in ORGANIZATION_NAMES:
            line += build_bullet_item_for_org(org_name);

    readme_file.write(line + "\n");

readme_file.close();
print "Done...";

## Commit
GIT_ADD    = "git add README.md"
GIT_COMMIT = "git commit -m \"[UpdateOrgsList] {0}\"".format(time.asctime())
GIT_PUSH   = "git push origin master";

os.chdir("..");
os.system(
    "{0} && {1}".format(
    GIT_ADD,
    GIT_COMMIT,
));

os.system(
    "{0}".format(GIT_PUSH)
);

