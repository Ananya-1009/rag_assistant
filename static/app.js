document.addEventListener("DOMContentLoaded",()=>{
    const button=document.getElementById("send-btn");
    button.addEventListener("click",()=>{
        const input=document.getElementById("message-input");
        const text=input.value.trim();
        if(!text){
            return;
        }
        const chat=document.getElementById("chat-window");
        const div=document.createElement("div");
        div.className="message user";
        div.innerText=text;
        chat.appendChild(div);
        input.value="";
        chat.scrollTop=chat.scrollHeight;
    });
});