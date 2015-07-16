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
  options.push_back("Peter (3.508)");
  options.push_back("Ray (3.512)");
  options.push_back("Dana (3.510)");
  options.push_back("Kazunori (3.402)");
  options.push_back("Matteo (3.418)");
  options.push_back("Shiqi (3.420)");
  options.push_back("Jivko (3.432)");
  options.push_back("Stacy (3.502)");
  options.push_back("BWI Lab");
  options.push_back("Robot Soccer Lab");
  options.push_back("Not on the list?");


  srv.request.type = 1; 
  srv.request.message = "Where do you need to go?"; 
  srv.request.options = options;
  srv.request.timeout = bwi_msgs::QuestionDialogRequest::NO_TIMEOUT; 
  gui_client.waitForExistence();
  gui_client.call(srv);

  switch(srv.response.index){
  	case 0:
  		location = "d3_508";
  		break;
  	case 1:
  		location = "d3_512";
  		break;
  	case 2:
  		location = "d3_510";
  		break;
  	case 3:
  		location = "d3_402";
  		break;
  	case 4:
  	    location = "d3_418";
  		break;
  	case 5:
  		location = "d3_420";
  		break;
  	case 6:
  		location = "d3_432";
  		break;
  	case 7:
  		location = "d3_502";
  		break;
  	case 8:
  		location = "d3_414b";
  		break;
  	case 9:
  		location = "d3_436";
  		break;
  }


  if (srv.response.index == 10) {
    srv.request.type = 2;
    srv.request.message = "What is the location? [ex. d3_414b or d3_418]"; 
    gui_client.call(srv);
    location = srv.response.text;
  }

  
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
