import os
from utils.logger import logger

# USERNAME = os.environ['USERNAME']
# TAGNAME = os.environ['TAGNAME']
# TAGVALUE = os.environ['TAGVALUE']
MODULE_VERSION = os.environ['MODULE_VERSION']
SNSARN = os.environ.get('SNSARN')
SSMROLE = os.environ['SSMROLE'] 


# TARGETS = [{
#     "Key": f"tag:{TAGNAME}",
#     "Values": [TAGVALUE]
# }]