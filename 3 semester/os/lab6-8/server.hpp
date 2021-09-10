#ifndef LAB6_8_SERVER_HPP
#define LAB6_8_SERVER_HPP

#include <zmqpp/zmqpp.hpp>
#include <unistd.h>
#include <iostream>
#include <string>
const std::string host = "tcp://127.0.0.1:";

void create_node(int& id, int& port, int& ping_port) {
    char* arg_node = strdup("./node");
    char* arg_id = strdup((std::to_string(id)).c_str());
    char* arg_port = strdup((std::to_string(port)).c_str());
    char* arg_ping_port = strdup((std::to_string(ping_port)).c_str());
    char* args[] = {arg_node, arg_id, arg_port, arg_ping_port, nullptr};
    execv("./node", args);
}

bool send_msg(zmqpp::socket& socket, const std::string& msg) {
    zmqpp::message message;
    message << msg;
    try {
        socket.send(message);
        return true;
    } catch(...) {
        return false;
    }
}

std::string recieve_msg(zmqpp::socket& socket) {
    zmqpp::message message;
    try {
        socket.receive(message);
    } catch(zmqpp::zmq_internal_exception& e) {
        message = false;
    }
    std::string answer;
    message >> answer;
    return answer;
}

int bind_socket(zmqpp::socket& socket) {
    int port = 3000;
    while (true) {
        try {
            socket.bind(host+std::to_string(port));
            break;
        } catch(zmqpp::zmq_internal_exception& e) {
            ++port;
        }
    }
    return port;
}
#endif 
