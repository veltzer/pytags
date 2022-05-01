import pyclassifiers.values
import config.general
import config.helpers

project_github_username = "veltzer"
project_name = "pytags"
github_repo_name = project_name
project_website = f"https://{project_github_username}.github.io/{project_name}"
project_website_source = f"https://github.com/{project_github_username}/{project_name}"
project_website_git = f"git://github.com/{project_github_username}/{project_name}.git"
project_website_download_ppa = "https://launchpanet/~mark-veltzer/+archive/ubuntu/ppa"
project_website_download_src = project_website_source
# noinspection SpellCheckingInspection
project_paypal_donate_button_id = "ASPRXR59H2NTQ"
project_google_analytics_tracking_id = "UA-56436979-1"
project_short_description = "module to help you tag interesting places in your code"
project_long_description = project_short_description
# keywords to put on html pages or for search, dont put the name of the project or my details
# as they will be added automatically...
project_keywords = [
    "pytags",
    "tag",
    "code",
    "command",
    "line",
]
project_license = "MIT"
project_year_started = 2012
project_description = project_short_description
project_platforms = [
    "python3",
]
project_classifiers = [
    pyclassifiers.values.DevelopmentStatus__4_Beta,
    pyclassifiers.values.Environment__Console,
    pyclassifiers.values.OperatingSystem__OSIndependent,
    pyclassifiers.values.ProgrammingLanguage__Python,
    pyclassifiers.values.ProgrammingLanguage__Python__3,
    pyclassifiers.values.ProgrammingLanguage__Python__3__Only,
    pyclassifiers.values.ProgrammingLanguage__Python__39,
    pyclassifiers.values.Topic__Utilities,
    pyclassifiers.values.License__OSIApproved__MITLicense,
]

project_data_files = []

codacy_id = None
project_google_analytics_tracking_id = None
project_paypal_donate_button_id = None

project_copyright_years = config.helpers.get_copyright_years(project_year_started)
project_google_analytics_snipplet = config.helpers.get_google_analytics(project_google_analytics_tracking_id)
project_paypal_donate_button_snipplet = config.helpers.get_paypal(project_paypal_donate_button_id)
