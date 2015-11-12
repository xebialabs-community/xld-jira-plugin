#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import base64
import httplib
import json
from urlparse import urlparse

class JiraCommunicator:
    """ Jira Communicator using REST API """

    def __init__(self, endpoint='http://localhost:4516', username='admin', password='admin', apiVersion='latest'):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.apiVersion = apiVersion

    def issue_exists(self,jira):
        print "Check Jira Issue [%s]" % jira
        try:
            self.do_get("/rest/api/%s/issue/%s" % (self.apiVersion,jira))
            print "Jira Issue [%s] exists" % jira
            return True
        except:
            return False

    def get_issue(self,jira):
        return self.do_get("/rest/api/%s/issue/%s" % (self.apiVersion,jira))

    def get_transitions_issue(self,jira):
        return self.do_get("/rest/api/%s/issue/%s/transitions" % (self.apiVersion,jira))

    def update_transition_issue(self,jira,doc):
        return self.do_post_no_parse("/rest/api/%s/issue/%s/transitions" % (self.apiVersion,jira), doc)

    def update_comment(self,jira,comment):
        print "Update comment %s : %s " % (jira,comment)
        commentData = {
                "body": comment
                }
        return self.do_post_no_parse("/rest/api/%s/issue/%s/comment" % (self.apiVersion,jira), json.dumps(commentData) )

    def move_issue_to_transistion(self,jira, transition_name, transition_message):
        jira_data_transitions = self.get_transitions_issue(jira)
        next_transitions = filter(lambda t: t['name'] == transition_name, jira_data_transitions['transitions'])
        if len(next_transitions) > 0:
            next_transition = next_transitions[0]
        else:
            raise ValueError('Transistion [%s] not found' % transition_name)

        print "Performing transition %s " % (transition_name)
        transitionData = {
                "transition": {
                    "id": next_transition['id']
                    }
                }

        self.update_transition_issue(jira,json.dumps(transitionData))

        self.update_comment(jira, transition_message )

    def do_get(self, path):
        return self.do_it("GET", path, "")

    def do_put(self, path, doc):
        return self.do_it("PUT", path, doc)

    def do_post(self, path, doc):
        return self.do_it("POST", path, doc)

    def do_post_no_parse(self, path, doc):
        return self.do_it("POST", path, doc, False)

    def do_delete(self, path):
        return self.do_it("DELETE", path, "", False)

    def do_it(self, verb, path, doc, parse_response=True):
        #print "DO %s %s on %s " % (verb, path, self.endpoint)

        parsed_url = urlparse(self.endpoint)
        if parsed_url.scheme == "https":
            conn = httplib.HTTPSConnection(parsed_url.hostname, parsed_url.port)
        else:
            conn = httplib.HTTPConnection(parsed_url.hostname, parsed_url.port)

        try:
            auth = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
            headers = {"content-type": "application/json", "Authorization": "Basic %s" % auth}

            conn.request(verb, path, doc, headers)
            response = conn.getresponse()
            #print response.status, response.reason
            if response.status != 200 and response.status != 204 and response.status !=201:
                raise Exception("Error when requesting XL Deploy Server [%s]:%s" % (response.status, response.reason))

            if parse_response:
                data = str(response.read())
                decoded = json.loads(data)
                return decoded
            return None
        finally:
            conn.close()


    def __str__(self):
        return "[endpoint=%s, username=%s]" % (self.endpoint, self.username)

