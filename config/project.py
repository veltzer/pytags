import datetime
import pyclassifiers.values
import config.general

project_github_username = 'veltzer'
project_name = 'pytags'
github_repo_name = project_name
project_website = 'https://{project_github_username}.github.io/{project_name}'.format(**locals())
project_website_source = 'https://github.com/{project_github_username}/{project_name}'.format(**locals())
project_website_git = 'git://github.com/{project_github_username}/{project_name}.git'.format(**locals())
project_website_download_ppa = 'https://launchpanet/~mark-veltzer/+archive/ubuntu/ppa'
project_website_download_src = project_website_source
# noinspection SpellCheckingInspection
project_paypal_donate_button_id = 'ASPRXR59H2NTQ'
project_google_analytics_tracking_id = 'UA-56436979-1'
project_short_description = 'module to help you tag interesting places in your code'
project_long_description = project_short_description
# keywords to put on html pages or for search, dont put the name of the project or my details
# as they will be added automatically...
project_keywords = [
    'pytags',
    'tag',
    'code',
    'command',
    'line',
]
project_license = 'MIT'
project_year_started = '2012'
project_description = project_short_description
project_platforms = [
    'python3',
]
project_classifiers = [
    pyclassifiers.values.DevelopmentStatus__4_Beta,
    pyclassifiers.values.Environment__Console,
    pyclassifiers.values.OperatingSystem__OSIndependent,
    pyclassifiers.values.ProgrammingLanguage__Python,
    pyclassifiers.values.ProgrammingLanguage__Python__3,
    pyclassifiers.values.ProgrammingLanguage__Python__3__Only,
    pyclassifiers.values.ProgrammingLanguage__Python__36,
    pyclassifiers.values.ProgrammingLanguage__Python__37,
    pyclassifiers.values.ProgrammingLanguage__Python__38,
    pyclassifiers.values.Topic__Utilities,
    pyclassifiers.values.License__OSIApproved__MITLicense,
]

project_data_files = []
# project_data_files.append(templar.utils.hlp_files_under('/usr/bin', 'src/*'))

project_copyright_years = ', '.join(
    map(str, range(int(project_year_started), datetime.datetime.now().year + 1)))
if str(config.general.general_current_year) == project_year_started:
    project_copyright_years_short = config.general.general_current_year
else:
    project_copyright_years_short = '{0}-{1}'.format(project_year_started, config.general.general_current_year)

project_google_analytics_snipplet = '''<script type="text/javascript">
(function(i,s,o,g,r,a,m){{i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){{
(i[r].q=i[r].q||[]).push(arguments)}},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
}})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', '{0}', 'auto');
ga('send', 'pageview');

</script>'''.format(project_google_analytics_tracking_id)
project_paypal_donate_button_snipplet = '''<form action="https://www.paypal.com/cgi-bin/webscr"
    method="post" target="_top">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="hosted_button_id" value="{0}">
<input type="image" src="https://www.paypalobjects.com/en_US/IL/i/btn/btn_donateCC_LG.gif" name="submit"
alt="PayPal - The safer, easier way to pay online!">
<img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">
</form>'''.format(project_paypal_donate_button_id)
