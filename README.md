# xld-jira-plugin
Integration between JIRA and XL Deploy

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

Place the plugin JAR file into your `SERVER_HOME/plugins` directory.

# Usage #

This is a sample of rules that are using the steps defined in this
plugin.

The rules are using the sample configuration define in the Release
Dashboard documentation : https://docs.xebialabs.com/xl-deploy/how-to/configure-the-release-dashboard.html. The target environment requires a Change Ticket Number.

The plugin define the JIRA info by adding 3 property to
`udm.Environment` CI.

```xl-rules-sample.xml```

```

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
          <url expression="true">specification.deployedOrPreviousApplication.environment.jiraUrl</url>
          <username expression="true">specification.deployedOrPreviousApplication.environment.jiraUsername</username>
          <password expression="true">specification.deployedOrPreviousApplication.environment.jiraPassword</password>
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
          <url expression="true">specification.deployedOrPreviousApplication.environment.jiraUrl</url>
          <username expression="true">specification.deployedOrPreviousApplication.environment.jiraUsername</username>
          <password expression="true">specification.deployedOrPreviousApplication.environment.jiraPassword</password>
          <next_transition_name>Ready for PROD</next_transition_name>
        </jython-context>
      </jython>
      <jython>
        <description expression="true">"Add a comment to [%s] ticket" % (specification.deployedOrPreviousApplication.version.satisfiesChangeTicketNumber)</description>
        <order>10</order>
        <script-path>xld/jira/comment.py</script-path>
        <jython-context>
          <jira expression="true">specification.deployedOrPreviousApplication.version.satisfiesChangeTicketNumber</jira>
          <url expression="true">specification.deployedOrPreviousApplication.environment.jiraUrl</url>
          <username expression="true">specification.deployedOrPreviousApplication.environment.jiraUsername</username>
          <password expression="true">specification.deployedOrPreviousApplication.environment.jiraPassword</password>
          <next_transition_name>Ready for PROD</next_transition_name>
          <message>Automaticaly Commented by XLDeploy 5.1.1</message>
        </jython-context>
      </jython>

    </steps>
  </rule>

```


