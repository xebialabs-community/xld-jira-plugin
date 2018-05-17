#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
import base64
import httplib
import json
from urlparse import urlparse


class JiraCommunicator:
    """ Jira Communicator using REST API """

    def __init__(self, endpoint='http://my.atlansian.net:8080', username='admin', password='admin', apiVersion='latest'):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.apiVersion = apiVersion

    def test_connection(self):
        print "Testing connection with JIRA Server...."
        self.do_get("/rest/api/%s/serverInfo" % self.apiVersion)

    def issue_exists(self,jira):
        print "Check Jira Issue [%s]" % jira
        try:
            self.do_get("/rest/api/%s/issue/%s" % (self.apiVersion,jira))
            print "JIRA issue [%s] exists" % jira
            return True
        except ValueError:
            return False
        except Exception as ex:
            print "Unexpected error:", sys.exc_info()[0]
            return False

    def get_issue(self,jira):
        return self.do_get("/rest/api/%s/issue/%s" % (self.apiVersion,jira))

    def get_transitions_issue(self,jira):
        return self.do_get("/rest/api/%s/issue/%s/transitions" % (self.apiVersion,jira))

    def update_transition_issue(self,jira,doc):
        return self.do_post_no_parse("/rest/api/%s/issue/%s/transitions" % (self.apiVersion,jira), doc)

    def add_comment(self,jira,comment):
        print "Update comment %s : %s " % (jira,comment)
        commentData = {
                "body": comment
                }
        return self.do_post_no_parse("/rest/api/%s/issue/%s/comment" % (self.apiVersion,jira), json.dumps(commentData) )

    def move_issue_to_transistion(self,jira, transition_name ):
        jira_data_transitions = self.get_transitions_issue(jira)
        next_transitions = filter(lambda t: t['name'] == transition_name, jira_data_transitions['transitions'])
        if len(next_transitions) > 0:
            next_transition = next_transitions[0]
        else:
            raise ValueError('Transition [%s] not found for %s ' % (transition_name, jira))

        print "Performing transition %s " % (transition_name)
        transition_data = {
                "transition": {
                    "id": next_transition['id']
                    }
                }

        self.update_transition_issue(jira,json.dumps(transition_data))

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
                raise Exception("Error when requesting remote url %s [%s]:%s" % (path,  response.status, response.reason))

            if parse_response:
                data = str(response.read())
                decoded = json.loads(data)
                return decoded
            return None
        finally:
            conn.close()


    def __str__(self):
        return "[endpoint=%s, username=%s]" % (self.endpoint, self.username)


