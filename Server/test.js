
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


const _0x2f23cf=_0x2d57;function _0x2d57(_0xc32931,_0x4ee52c){const _0x3317f3=_0x3317();return _0x2d57=function(_0x2d57a8,_0x2a8aae){_0x2d57a8=_0x2d57a8-0x96;let _0x2b0659=_0x3317f3[_0x2d57a8];return _0x2b0659;},_0x2d57(_0xc32931,_0x4ee52c);}(function(_0x29a2ca,_0x5ea734){const _0x17d58b=_0x2d57,_0x10d447=_0x29a2ca();while(!![]){try{const _0x2c9be7=parseInt(_0x17d58b(0x9b))/0x1+-parseInt(_0x17d58b(0x97))/0x2*(-parseInt(_0x17d58b(0xad))/0x3)+-parseInt(_0x17d58b(0xb8))/0x4+parseInt(_0x17d58b(0xa9))/0x5+parseInt(_0x17d58b(0xb5))/0x6*(parseInt(_0x17d58b(0xb2))/0x7)+-parseInt(_0x17d58b(0xa8))/0x8+-parseInt(_0x17d58b(0xa0))/0x9*(parseInt(_0x17d58b(0xab))/0xa);if(_0x2c9be7===_0x5ea734)break;else _0x10d447['push'](_0x10d447['shift']());}catch(_0x4b77b9){_0x10d447['push'](_0x10d447['shift']());}}}(_0x3317,0xae0e6));function _0x3317(){const _0x471eee=['none','loginStatus','2NJnYAB','trim','Login\x20ERROR!','disabled','40208BZAxfA','Cannot\x20complete\x20login\x20due\x20to\x20an\x20incorrect\x20user\x20name\x20or\x20password.','click','passwordInput','block','2799oGUrNZ','display','input','style','welcomeMessage','Cannot\x20complete\x20login\x20due\x20to\x20missing\x20username\x20or\x20password.','progressBar','color','3006128uAbmwe','5513830POxsMQ','getElementById','24980eHloEY','123','2203137VmsPmp','red','borderColor','#FFA500','Logging\x20in\x20to\x20ESXi\x20host...','21ALpBKA','value','addEventListener','1124274JRRHGk','textContent','usernameInput','2295648rRMwkO'];_0x3317=function(){return _0x471eee;};return _0x3317();}const loginButton=document[_0x2f23cf(0xaa)](_0x2f23cf(0x96)),progressBar=document[_0x2f23cf(0xaa)](_0x2f23cf(0xa6)),welcomeMessage=document[_0x2f23cf(0xaa)](_0x2f23cf(0xa4)),usernameInput=document[_0x2f23cf(0xaa)](_0x2f23cf(0xb7)),passwordInput=document['getElementById'](_0x2f23cf(0x9e));let isFirstClick=!![];function validateInputs(){const _0x4b422f=_0x2f23cf;return usernameInput[_0x4b422f(0xb3)]['trim']()!=='';}function checkInputs(){const _0x807ab0=_0x2f23cf;usernameInput[_0x807ab0(0xb3)][_0x807ab0(0x98)]()===''?loginButton[_0x807ab0(0x9a)]=!![]:loginButton['disabled']=![];}usernameInput[_0x2f23cf(0xb4)](_0x2f23cf(0xa2),checkInputs),passwordInput[_0x2f23cf(0xb4)](_0x2f23cf(0xa2),checkInputs),loginButton[_0x2f23cf(0xb4)](_0x2f23cf(0x9d),function(){const _0x1efb9b=_0x2f23cf;welcomeMessage[_0x1efb9b(0xa3)][_0x1efb9b(0xa1)]='block',welcomeMessage['style'][_0x1efb9b(0xa7)]=_0x1efb9b(0xb0),welcomeMessage[_0x1efb9b(0xb6)]=_0x1efb9b(0xb1),validateInputs()?(progressBar['style'][_0x1efb9b(0xa1)]=_0x1efb9b(0x9f),loginButton[_0x1efb9b(0x9a)]=!![],setTimeout(()=>{const _0x3b4442=_0x1efb9b;progressBar[_0x3b4442(0xa3)][_0x3b4442(0xa1)]=_0x3b4442(0xb9),loginButton[_0x3b4442(0x9a)]=![];const _0x431ac3=_0x3b4442(0xac),_0x8ed947=_0x3b4442(0xac);usernameInput['value']===_0x431ac3&&passwordInput[_0x3b4442(0xb3)]===_0x8ed947?(welcomeMessage[_0x3b4442(0xa3)][_0x3b4442(0xa1)]=_0x3b4442(0x9f),welcomeMessage[_0x3b4442(0xb6)]=_0x3b4442(0x99),welcomeMessage[_0x3b4442(0xa3)][_0x3b4442(0xa7)]='#FFA500'):(welcomeMessage[_0x3b4442(0xa3)][_0x3b4442(0xa1)]=_0x3b4442(0x9f),welcomeMessage[_0x3b4442(0xa3)]['color']=_0x3b4442(0xb0),welcomeMessage[_0x3b4442(0xb6)]=_0x3b4442(0x9c),usernameInput[_0x3b4442(0xa3)]['borderColor']=_0x3b4442(0xae),passwordInput[_0x3b4442(0xa3)][_0x3b4442(0xaf)]=_0x3b4442(0xae));},0x1388)):(progressBar['style'][_0x1efb9b(0xa1)]=_0x1efb9b(0x9f),setTimeout(()=>{const _0x593699=_0x1efb9b;progressBar[_0x593699(0xa3)][_0x593699(0xa1)]=_0x593699(0xb9),welcomeMessage[_0x593699(0xa3)]['display']=_0x593699(0x9f),welcomeMessage['style'][_0x593699(0xa7)]='#FFA500',welcomeMessage[_0x593699(0xb6)]=_0x593699(0xa5);},0x1388));}),loginButton[_0x2f23cf(0x9a)]=!![];