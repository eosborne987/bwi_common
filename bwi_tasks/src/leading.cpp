#include "bwi_kr_execution/ExecutePlanAction.h"
#include "bwi_msgs/QuestionDialog.h"
#include <actionlib/client/simple_action_client.h>
#include <ros/ros.h>
#include <string>
#include <iostream>

typedef actionlib::SimpleActionClient<bwi_kr_execution::ExecutePlanAction> Client;

using namespace std; 

int main(int argc, char**argv) {
  ros::init(argc, argv, "leading");
  ros::NodeHandle n;
  
  ros::NodeHandle privateNode("~");
  string location;
  privateNode.param<string>("location",location,"");

  // GUI Client
  ros::ServiceClient gui_client = n.serviceClient<bwi_msgs::QuestionDialog>("question_dialog"); 

  ros::Duration(0.5).sleep(); 
  bwi_msgs::QuestionDialog srv;

  vector<std::string> options;

  srv.request.type = 2;
  srv.request.message = "What is the location? [ex. d3_414b or d3_418]\n"
    					"Peter (d3_508)\n"
    					"Ray (d3_512)\n"
    					"Dana (d3_510)\n"
    					"Kazunori (d3_402)\n"
    					"Matteo (d3_418)\n"
    					"Shiqi (d3_420)\n"
    					"Jivko (d3_432)\n"
    					"Stacy (d3_502)\n"
    					"BWI Lab (d3_414b)\n"
    					"Robot Soccer Lab\n"; 
    gui_client.call(srv);
    location = srv.response.text;


  
  // Create rule and goal
  Client client("action_executor/execute_plan", true);
  client.waitForServer();
  
  bwi_kr_execution::ExecutePlanGoal goal;
  
  bwi_kr_execution::AspRule rule;
  bwi_kr_execution::AspFluent gfluent;
  gfluent.name = "not facing";
  
  gfluent.variables.push_back(location);
 
  rule.body.push_back(gfluent);
  goal.aspGoal.push_back(rule);
  
  ROS_INFO("sending goal");
  client.sendGoal(goal);
  
  ros::Rate wait_rate(10);
  while(ros::ok() && !client.getState().isDone()) {
    wait_rate.sleep();
  }


  if (!client.getState().isDone()) {
    ROS_INFO("Canceling goal");
    client.cancelGoal();
    //and wait for canceling confirmation
    for(int i = 0; !client.getState().isDone() && i<50; ++i)
      wait_rate.sleep();
  }
  if (client.getState() == actionlib::SimpleClientGoalState::ABORTED) {
    ROS_INFO("Aborted");
  }
  else if (client.getState() == actionlib::SimpleClientGoalState::PREEMPTED) {
    ROS_INFO("Preempted");
  }
  else if (client.getState() == actionlib::SimpleClientGoalState::SUCCEEDED) {
    ROS_INFO("Succeeded!");
  }
  else {
     ROS_INFO("Terminated");
  }
    
  return 0;
}
