
// const loginButton = document.getElementById("loginStatus");
// const progressBar = document.getElementById("progressBar");
// const welcomeMessage = document.getElementById("welcomeMessage");
// const usernameInput = document.getElementById("usernameInput");
// const passwordInput = document.getElementById("passwordInput");

// let isFirstClick = true;

// function validateInputs() {
//     return usernameInput.value.trim() !== "";
// }

// function checkInputs() {
//         if (usernameInput.value.trim() === "" ) {
//             loginButton.disabled = true;
//         } else {
//             loginButton.disabled = false;
//         }
//     }

// usernameInput.addEventListener("input", checkInputs);
// passwordInput.addEventListener("input", checkInputs);

// loginButton.addEventListener("click", function () {
    
//     welcomeMessage.style.display = "block";
//     welcomeMessage.style.color = "#FFA500";
//     welcomeMessage.textContent = "Logging in to ESXi host...";

//     if (validateInputs()) {
//         progressBar.style.display = "block";
//         loginButton.disabled = true;

//         setTimeout(() => {
//             progressBar.style.display = "none";
//             loginButton.disabled = false;

//             const correctUsername = "123"; // Replace with your actual username
//             const correctPassword = "123"; // Replace with your actual password

//             if (usernameInput.value === correctUsername && passwordInput.value === correctPassword) {
//                 welcomeMessage.style.display = "block";
//                 welcomeMessage.textContent = "Login ERROR!"   ;
//                 welcomeMessage.style.color = "#FFA500";
//             } else {
//                 welcomeMessage.style.display = "block";
//                 welcomeMessage.style.color = "#FFA500";
//                 welcomeMessage.textContent = "Cannot complete login due to an incorrect user name or password.";
//                 usernameInput.style.borderColor = "red"
//                 passwordInput.style.borderColor = "red"
//             }

            
//         }, 5000); // Simulate a 3-second login process
//     } else {
//         progressBar.style.display = "block";

//         setTimeout(() => {
//             progressBar.style.display = "none";
//             welcomeMessage.style.display = "block";
//             welcomeMessage.style.color = "#FFA500";
//             welcomeMessage.textContent = "Cannot complete login due to missing username or password.";
//         }, 5000); // Simulate a 3-second process
//     }
// });

// loginButton.disabled = true;
// // nếu nhập sai hoặc nhập thiếu thì thời gian chạy khoảng 5s
// // nếu nhập đúng thì thời gian chạy từ 13-18s hiển thị "Conection Timeout" hoặc "Kết nối bị gián đoạn"




const _0x4ccc1a=_0x368c;(function(_0x52a887,_0x39a074){const _0x46775e=_0x368c,_0x449da6=_0x52a887();while(!![]){try{const _0x5e6115=parseInt(_0x46775e(0x1d3))/0x1+-parseInt(_0x46775e(0x1d0))/0x2*(-parseInt(_0x46775e(0x1e6))/0x3)+-parseInt(_0x46775e(0x1e2))/0x4*(-parseInt(_0x46775e(0x1e0))/0x5)+parseInt(_0x46775e(0x1d5))/0x6*(-parseInt(_0x46775e(0x1ec))/0x7)+-parseInt(_0x46775e(0x1e3))/0x8*(-parseInt(_0x46775e(0x1d9))/0x9)+parseInt(_0x46775e(0x1e9))/0xa+-parseInt(_0x46775e(0x1cf))/0xb;if(_0x5e6115===_0x39a074)break;else _0x449da6['push'](_0x449da6['shift']());}catch(_0x368dce){_0x449da6['push'](_0x449da6['shift']());}}}(_0x4936,0xc7196));function _0x4936(){const _0xfd7c04=['welcomeMessage','8634790DCfZtv','borderColor','none','7zQhzlQ','usernameInput','progressBar','trim','123','3913525jBtFQg','64364xNBXMO','red','disabled','337463RLBWWM','addEventListener','5244654OAExIk','passwordInput','textContent','display','1505511MVkiYE','value','Logging\x20in\x20to\x20ESXi\x20host...','Login\x20ERROR!','input','#FFA500','click','5BAAUps','block','262860OJMVMR','8wXSQnH','style','color','57wYCRCD','getElementById'];_0x4936=function(){return _0xfd7c04;};return _0x4936();}const loginButton=document[_0x4ccc1a(0x1e7)]('loginStatus'),progressBar=document['getElementById'](_0x4ccc1a(0x1cc)),welcomeMessage=document[_0x4ccc1a(0x1e7)](_0x4ccc1a(0x1e8)),usernameInput=document[_0x4ccc1a(0x1e7)](_0x4ccc1a(0x1cb)),passwordInput=document[_0x4ccc1a(0x1e7)](_0x4ccc1a(0x1d6));let isFirstClick=!![];function _0x368c(_0x539534,_0x1b6640){const _0x4936f6=_0x4936();return _0x368c=function(_0x368c47,_0x46d625){_0x368c47=_0x368c47-0x1cb;let _0x2b4b16=_0x4936f6[_0x368c47];return _0x2b4b16;},_0x368c(_0x539534,_0x1b6640);}function validateInputs(){const _0x5d2802=_0x4ccc1a;return usernameInput[_0x5d2802(0x1da)][_0x5d2802(0x1cd)]()!=='';}function checkInputs(){const _0x324476=_0x4ccc1a;usernameInput['value'][_0x324476(0x1cd)]()===''?loginButton[_0x324476(0x1d2)]=!![]:loginButton[_0x324476(0x1d2)]=![];}usernameInput[_0x4ccc1a(0x1d4)]('input',checkInputs),passwordInput[_0x4ccc1a(0x1d4)](_0x4ccc1a(0x1dd),checkInputs),loginButton[_0x4ccc1a(0x1d4)](_0x4ccc1a(0x1df),function(){const _0x22e5cf=_0x4ccc1a;welcomeMessage[_0x22e5cf(0x1e4)][_0x22e5cf(0x1d8)]=_0x22e5cf(0x1e1),welcomeMessage[_0x22e5cf(0x1e4)][_0x22e5cf(0x1e5)]=_0x22e5cf(0x1de),welcomeMessage[_0x22e5cf(0x1d7)]=_0x22e5cf(0x1db),validateInputs()?(progressBar['style']['display']=_0x22e5cf(0x1e1),loginButton[_0x22e5cf(0x1d2)]=!![],setTimeout(()=>{const _0x1a7e9d=_0x22e5cf;progressBar[_0x1a7e9d(0x1e4)][_0x1a7e9d(0x1d8)]=_0x1a7e9d(0x1eb),loginButton[_0x1a7e9d(0x1d2)]=![];const _0x27eb55=_0x1a7e9d(0x1ce),_0x570d72=_0x1a7e9d(0x1ce);usernameInput['value']===_0x27eb55&&passwordInput[_0x1a7e9d(0x1da)]===_0x570d72?(welcomeMessage[_0x1a7e9d(0x1e4)]['display']=_0x1a7e9d(0x1e1),welcomeMessage[_0x1a7e9d(0x1d7)]=_0x1a7e9d(0x1dc),welcomeMessage[_0x1a7e9d(0x1e4)]['color']=_0x1a7e9d(0x1de)):(welcomeMessage[_0x1a7e9d(0x1e4)][_0x1a7e9d(0x1d8)]=_0x1a7e9d(0x1e1),welcomeMessage[_0x1a7e9d(0x1e4)][_0x1a7e9d(0x1e5)]='#FFA500',welcomeMessage[_0x1a7e9d(0x1d7)]='Cannot\x20complete\x20login\x20due\x20to\x20an\x20incorrect\x20user\x20name\x20or\x20password.',usernameInput[_0x1a7e9d(0x1e4)][_0x1a7e9d(0x1ea)]='red',passwordInput[_0x1a7e9d(0x1e4)]['borderColor']=_0x1a7e9d(0x1d1));},0x1388)):(progressBar[_0x22e5cf(0x1e4)][_0x22e5cf(0x1d8)]=_0x22e5cf(0x1e1),setTimeout(()=>{const _0x23f228=_0x22e5cf;progressBar[_0x23f228(0x1e4)][_0x23f228(0x1d8)]=_0x23f228(0x1eb),welcomeMessage[_0x23f228(0x1e4)]['display']='block',welcomeMessage[_0x23f228(0x1e4)][_0x23f228(0x1e5)]=_0x23f228(0x1de),welcomeMessage[_0x23f228(0x1d7)]='Cannot\x20complete\x20login\x20due\x20to\x20missing\x20username\x20or\x20password.';},0x1388));}),loginButton['disabled']=!![];
