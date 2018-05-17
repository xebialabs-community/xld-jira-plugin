# XL Deploy Jira plugin

[![Build Status][xld-jira-plugin-travis-image]][xld-jira-plugin-travis-url]
[![License: MIT][xld-jira-plugin-license-image]][xld-jira-plugin-license-url]
![Github All Releases][xld-jira-plugin-downloads-image]

[xld-jira-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xld-jira-plugin.svg?branch=master
[xld-jira-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xld-jira-plugin
[xld-jira-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xld-jira-plugin-license-url]: https://opensource.org/licenses/MIT
[xld-jira-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xld-jira-plugin/total.svg

# Preface #

This document describes the functionality provided by the XLD JIRA plugin.

See the **XL Deploy Reference Manual** for background information on XL Deploy and deployment concepts.

# Overview #

This plugin offers sample steps to

* Check a JIRA ticket exists.
* Change the transition to another state.
* Add a comment to a JIRA ticket.

# Requirements #

* **Requirements**
	* **XL Deploy** 4.5.0
	* **JIRA**

# Installation #

* Copy the latest JAR or XLDP file from the [releases page](https://github.com/xebialabs-community/xld-jira-plugin/releases) into the `XL_DEPLOY_SERVER/plugins` directory.
* Restart the XL Deploy server.

# Usage #

This is a sample of rules that are using the steps defined in this plugin.

The rules are using the sample configuration define in the Release Dashboard documentation : https://docs.xebialabs.com/xl-deploy/how-to/configure-the-release-dashboard.html. The target environment requires a Change Ticket Number.

The plugin defines the JIRA information (url, username, password) in the 'Configuration' Node and add 1 property to `udm.Environment` CI.

```xl-rules-sample.xml```

```xml
 <rule name="xl.DeployToProduction.checkJira" scope="pre-plan">
    <conditions>
      <expression>specification.deployedOrPreviousApplication.environment.requiresChangeTicketNumber</expression>
    </conditions>
    <steps>
      <jython>
        <description expression="true">"Check if the [%s] Ticket is valid" % (specification.deployedOrPreviousApplication.version.satisfiesChangeTicketNumber)</description>
        <order>10</order>
        <script-path>xld/jira/check.py</script-path>
        <jython-context>
          <jira expression="true">specification.deployedOrPreviousApplication.version.satisfiesChangeTicketNumber</jira>
          <server expression="true">specification.deployedOrPreviousApplication.environment.jiraServer</server>          
        </jython-context>
      </jython>
    </steps>
  </rule>
  <rule name="xl.DeployToProduction.updateJira" scope="post-plan">
    <conditions>
      <expression>specification.deployedOrPreviousApplication.environment.requiresChangeTicketNumber</expression>
    </conditions>
    <steps>
      <jython>
        <description expression="true">"update The [%s] Ticket status" % (specification.deployedOrPreviousApplication.version.satisfiesChangeTicketNumber)</description>
        <order>10</order>
        <script-path>xld/jira/transition.py</script-path>
        <jython-context>
          <jira expression="true">specification.deployedOrPreviousApplication.version.satisfiesChangeTicketNumber</jira>
          <server expression="true">specification.deployedOrPreviousApplication.environment.jiraServer</server>
          <next_transition_name>Ready for PROD</next_transition_name>
        </jython-context>
      </jython>
      <jython>
        <description expression="true">"Add a comment to [%s] ticket" % (specification.deployedOrPreviousApplication.version.satisfiesChangeTicketNumber)</description>
        <order>10</order>
        <script-path>xld/jira/comment.py</script-path>
        <jython-context>
          <jira expression="true">specification.deployedOrPreviousApplication.version.satisfiesChangeTicketNumber</jira>
          <server expression="true">specification.deployedOrPreviousApplication.environment.jiraServer</server>          
          <message>Automatically Commented by XLDeploy 5.1.1</message>
        </jython-context>
      </jython>
    </steps>
  </rule>
```


