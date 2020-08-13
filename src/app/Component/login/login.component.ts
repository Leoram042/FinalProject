import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
    selector: 'app-number',
    template:`<div class="col-sm-6">
    <form [formGroup]="LoginForm">
        <div class="form-group">
          Enter Your PhoneNumber : 
           <input type="text" id="phonenumber" class="form-control" formControlName="phonenumber"><br/>
            <span class="error" *ngIf="phonenumber.touched && phonenumber.invalid" style="color: red;">***PhoneNumber is invalid</span><br/>
            Enter Your OTP :
            <input type="text" id="otp" class="form-control" formControlName="otp"><br/>
            <span class="error" *ngIf="otp.touched && otp.invalid" style="color: red;">***OTP is invalid</span><br/>
            <button (click)="generateOTP()">Generate OTP</button>&nbsp;
            <button (click)="login()">Login</button>
        </div>
    </form>
</div>`
})
export class LoginComponent  {
  //anytxtUI : string
  LoginForm= new FormGroup({
    phonenumber: new FormControl('',[Validators.required, Validators.maxLength(10),Validators.pattern("(0/91)?[7-9][0-9]{9}")]),
    otp: new FormControl('',[Validators.required, Validators.maxLength(6)])
  })
  get phonenumber()
  {
    return this.LoginForm.get('phonenumber')
  }
  get otp()
  {
    return this.LoginForm.get('otp')
  }
  generateOTP(){
    console.log(this.LoginForm.value);
  }
  login(){
    console.log(this.LoginForm.value);
  
  }
}