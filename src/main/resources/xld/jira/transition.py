#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from xld.jira.jiracommunicator import communicator

communicator = communicator.JiraCommunicator(url,username, password)
if not communicator.issue_exists(jira):
    raise ValueError("[%s] Not Found in %s" % (jira, communicator))
communicator.move_issue_to_transistion(jira,next_transition_name )

print "Done."
