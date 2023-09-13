from dotenv import load_dotenv
from dotenv import dotenv_values
import os
import sys

from api import Gitlab_API


if __name__ == "__main__":
    load_dotenv()
    # print()

    config = dotenv_values(".env")

    gitlab_api = Gitlab_API()

    print("--", len(sys.argv))


    if len(sys.argv) > 1:
        print(len(sys.argv))
        print("Parameters needed: <project id>")
        print(sys.argv)
        # project = gitlab_api.get_project(sys.argv[1])
        project_id = sys.argv[1]

        # sys.exit()
    else:
        print("default is project 13")
        project_id = 13

    print("project is for lookup", project_id)


    try:
        project = gitlab_api.get_project(project_id)

        print("\n")
        print("===========PROJECT=================\n")

        print("project id: ", project.id)
        print("project name: ", project.name)
        print("project description: ", project.description)
        print("project stars: ", project.star_count)
        print("project forks: ", project.forks_count)
        print("LFS enabled: ", project.lfs_enabled)
        print("creator id: ", project.creator_id)
        print("created at: ", project.created_at)

        print("\n")
    except Exception as e:
        print(e)
        sys.exit()

    try:
        user = gitlab_api.get_user(project.owner.id)

        print("===========USER=================\n")

        # print(user)
        print("name: ", user.name)
        print("username: ", user.username)
        print("user id: ", user.id)
        print("email: ", user.email)
        print("IP: ", user.last_sign_in_ip)
        print("gravatar URL: ", user.avatar_url)

        print("\n")


    except Exception as e:
        print("no user found")
        print(e)
        sys.exit()



    try:
        pipeline = gitlab_api.get_latest_pipeline(project_id)

        print("===========PIPELINE=================\n")

        print("id: ", pipeline.id)
        print("status: ", pipeline.status)
        print("created at: ", pipeline.created_at)
        print("finished at: ", pipeline.finished_at)
        print("pipeline coverage: ", pipeline.coverage)
        print("duration: ", pipeline.duration)
        # print("detailed status: ", pipeline.detailed_status)
        print("user started pipeline: ", pipeline.user.name)
        print("\n")
    except Exception as e:
        print(e)
        sys.exit()


    try:
        latest_pipeline = pipeline.id
        report = gitlab_api.get_test_report(13, latest_pipeline)

        # print("report", report)

        print("===========TEST REPORTS=================\n")

        print("successfull tests: ", report.success_count)
        print("failed tests: ", report.failed_count)
        # print(report.test_suites)

        print("\n")

        for suite in report.test_suites:
            print("name: ", suite.name)
            for case in suite.test_cases:
                print("test name: ", case.name)
                print("status: ", case.status)
                print("\n")

        print("\n")
    except Exception as e:
        print(e)
        sys.exit()

    try:
        test_summary = gitlab_api.get_test_summary(13, latest_pipeline)

        # print(test_summary)
        print("===========TEST REPORTS SUMMARY=================\n")

        print("sucessful tests: ", test_summary.total.success)
        print("failed tests: ", test_summary.total.failed)
        for suites in test_summary.test_suites:
            print(suites.name)
    except Exception as e:
        print(e)
        sys.exit()



