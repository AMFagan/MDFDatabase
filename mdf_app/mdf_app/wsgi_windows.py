activate_this = 'C:/Users/hwb14182/Envs/mdf_app/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/Users/hwb14182/Envs/mdf_app/Lib/site-packages')




# Add the app's directory to the PYTHONPATH
sys.path.append('C:/Users/hwb14182/mdf_app')
sys.path.append('C:/Users/hwb14182/mdf_app/mdf_app')

os.environ['DJANGO_SETTINGS_MODULE'] = 'mdf_app.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mdf_app.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()