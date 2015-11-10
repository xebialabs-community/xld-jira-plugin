from jira.jiracommunicator import communicator

next_transition_name="Ready for PROD"
next_transition_message = "Automaticaly Commented by XLDeploy"
communicator = communicator.JiraCommunicator(url,username, password)
if not communicator.issue_exists(jira):
    raise ValueError("[%s] Not Found in %s" % (jira, communicator))
communicator.move_issue_to_transistion(jira,next_transition_name, next_transition_message)

print "Done."
