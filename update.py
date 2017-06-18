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

################################################################################
## Imports                                                                    ##
################################################################################
import os;
import os.path;
import urllib;
import json;
import time;
import sys;


################################################################################
## Vars                                                                       ##
################################################################################
kBase_Url = "https://api.github.com/users/{ORGANIZATION_NAME}/repos"

kOrganization_Names = [
    "AmazingCow-Game-Core",
    "AmazingCow-Game-Framework",
    "AmazingCow-Game-Tool",
    "AmazingCow-Game",
    "AmazingCow-Libs",
    "AmazingCow-Tools",
    ## "AmazingCow-Imidiar",
];


################################################################################
## Functions                                                                  ##
################################################################################
def fetch_repos(organization_name):
    url      = kBase_Url.format(ORGANIZATION_NAME=organization_name);
    response = urllib.urlopen(url);
    data     = json.loads(response.read());


    print "Fetching repos for: ({0})".format(organization_name);
    repos = [];
    for info in data:
        repos.append({
            "name" : info["name"     ],
            "url"  : info["clone_url"]
        });

    print "Done... Found ({0}) repos.".format(len(repos));
    return repos;

def commit_changes(org_list_path):
    cwd = os.getcwd();

    os.chdir(org_list_path);
    print "CWD: ", os.getcwd();

    add_cmd    = "git add README.md";
    commit_cmd = "git commit -m \"- [UpdateOrgsList] Time: {0}\"".format(
        time.asctime(time.localtime())
    );
    push_cmd = "git push origin master";

    os.system("git status");
    os.system(add_cmd   );
    os.system(commit_cmd);
    os.system(push_cmd  );

    os.chdir(cwd);

def build_list_repo_name_for_org(org_name):
    ## AmazingCow-Game-Core -> Game-Core-List
    return org_name.replace("AmazingCow-", "") + "-List";

def build_url_for_org(org_name):
    return "https://github.com/{0}".format(org_name);

def build_trello_url_for_org(org_name):
    clean_name = org_name.lower().replace("-","");
    return "https://trello.com/{0}".format(clean_name);

def build_bullet_item_for_repo(repo_info):
    return "* [{0}]({1})\n".format(repo_info["name"], repo_info["url"]);

def build_bullet_item_for_org(org_name):
    return "* [{0}]({1})\n".format(org_name, build_url_for_org(org_name));

def canonize_path(path):
    return os.path.abspath(os.path.expanduser(path));

def replace_template(org_name, repos_info):
    template_lines = open("template.md").readlines();
    replaced_lines = [];

    for line in template_lines:
        line = line.replace("\n", "");

        if("__ORGANIZATION_NAME__" in line):
            line = line.replace("__ORGANIZATION_NAME__", org_name);

        if("__ORGANIZATION_URL__" in line):
            line = line.replace("__ORGANIZATION_URL__", build_url_for_org(org_name));

        if("__REPOS_LIST__" in line):
            line = "";
            for repo_info in repos_info:
                line += build_bullet_item_for_repo(repo_info);

        if("__TRELLO_URL__" in line):
            line = line.replace("__TRELLO_URL__", build_trello_url_for_org(org_name));

        if("__ALL_ORGANIZATIONS__" in line):
            line = "";
            for name in kOrganization_Names:
                line += build_bullet_item_for_org(name);

        replaced_lines.append(line);

    return "\n".join(replaced_lines);


################################################################################
## Script                                                                     ##
################################################################################
def main():
    base_path = canonize_path(sys.argv[1]);
    print "Base Path:", base_path;

    ## Iterate all AmazingCow organizations and build
    ## the organization README list.
    for org_name in kOrganization_Names:
        org_list_name = build_list_repo_name_for_org(org_name);
        org_list_path = os.path.join(base_path, org_list_name);

        print "Org Name      :", org_name;
        print "Org List Name :", org_list_name;
        print "Org List Path :", org_list_path;

        ## Get the repos from github and build the README.md contents.
        repos         = fetch_repos(org_name);
        replaced_text = replace_template(org_name, repos);

        ## Write the README.md.
        readme_fullpath = os.path.join(org_list_path, "README.md");
        readme_file     = open(readme_fullpath, "w");

        readme_file.write(replaced_text);
        readme_file.close();

        ## Commit
        commit_changes(org_list_path);

if __name__ == '__main__':
    main();
