"use client";

import { KeyboardEvent, useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

type Provider = { name: string; enabled: boolean; notes: string };
type Message = { role: 'user' | 'assistant'; text: string; imageData?: string };
type Conversation = { id:string; title:string; mode:string; updated_at:string; message_count:number };
const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1';
const modes = [['Auto','spark'],['Chat','chat'],['Coding','code'],['PDF','file'],['PPT','screen'],['Image','image'],['Search','globe']];
const modeModels: Record<string,string> = {
  Auto:'OpenRouter Auto', Chat:'OpenRouter Auto', Coding:'Qwen3 Coder Next',
  PDF:'OpenRouter Auto - Document', PPT:'OpenRouter Auto - Slides',
  Image:'Gemini 3.1 Flash Lite Image', Search:'Perplexity Sonar - Live Search',
};

function Icon({ name, size = 19 }: { name: string; size?: number }) {
  const p: Record<string, React.ReactNode> = {
    panel:<><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16"/></>,
    edit:<><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L8 18l-4 1 1-4Z"/></>,
    chat:<path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z"/>,
    spark:<path d="m13 2-2 8H4l7 4-2 8 11-12h-7Z"/>,
    code:<><path d="m8 9-4 3 4 3m8-6 4 3-4 3M14 5l-4 14"/></>,
    file:<><path d="M6 2h9l5 5v15H6Z"/><path d="M14 2v6h6M9 13h6m-6 4h6"/></>,
    screen:<><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 22h8m-4-4v4"/></>,
    image:<><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 15-5-5L5 20"/></>,
    globe:<><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18m0-18a14 14 0 0 0 0 18"/></>,
    clip:<path d="m21 12-9 9a6 6 0 0 1-8-9l10-10a4 4 0 0 1 5 6l-9 10a2 2 0 0 1-3-3l9-9"/>,
    mic:<><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0 0 14 0m-7 7v5"/></>,
    send:<><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></>,
    logout:<><path d="m10 17 5-5-5-5m5 5H3"/><path d="M14 3h7v18h-7"/></>,
    link:<><path d="M10 13a5 5 0 0 0 8 0l2-2a5 5 0 0 0-7-7l-2 2"/><path d="M14 11a5 5 0 0 0-8 0l-2 2a5 5 0 0 0 7 7l2-2"/></>,
    menu:<path d="M4 7h16M4 12h16M4 17h16"/>,
    copy:<><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M15 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h3"/></>,
    trash:<><path d="M4 7h16M9 7V4h6v3m3 0-1 14H7L6 7"/><path d="M10 11v6m4-6v6"/></>,
  };
  return <svg aria-hidden viewBox="0 0 24 24" width={size} height={size} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">{p[name]}</svg>;
}

function FormattedText({text,copyable}:{text:string;copyable:boolean}) {
  const [copied,setCopied]=useState(false);
  async function copyMarkdown(){
    await navigator.clipboard.writeText(text);
    setCopied(true);
    window.setTimeout(()=>setCopied(false),1600);
  }
  return <div className="markdown-response">
    <ReactMarkdown remarkPlugins={[remarkGfm]} components={{
      a:({children,...props})=><a {...props} target="_blank" rel="noreferrer">{children}</a>,
    }}>{text}</ReactMarkdown>
    {copyable&&<button className="copy-response" onClick={copyMarkdown} aria-label="Copy response as Markdown"><Icon name="copy" size={15}/>{copied?'Copied':'Copy Markdown'}</button>}
  </div>;
}

export default function HomePage() {
  const [input,setInput] = useState('');
  const [messages,setMessages] = useState<Message[]>([{role:'assistant',text:'Hello. How can I assist you today?'}]);
  const [conversations,setConversations] = useState<Conversation[]>([]);
  const [activeId,setActiveId] = useState<string|null>(null);
  const [activeTitle,setActiveTitle] = useState('New chat');
  const [mode,setMode] = useState('Chat');
  const [ready,setReady] = useState<boolean|null>(null);
  const [loading,setLoading] = useState(false);
  const [menu,setMenu] = useState(false);
  const [attachment,setAttachment] = useState<{name:string;text:string}|null>(null);
  const [listening,setListening] = useState(false);
  const list = useRef<HTMLDivElement>(null);
  const fileInput = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch(`${API}/chat/providers`).then(r => r.ok ? r.json() : Promise.reject())
      .then((data:Provider[]) => setReady(Boolean(data.find(p => p.name === 'openrouter')?.enabled)))
      .catch(() => setReady(false));
    void loadConversations(true);
  },[]);
  useEffect(() => {
    list.current?.scrollTo({ top: list.current.scrollHeight, behavior: 'smooth' });
  }, [messages, loading]);

  async function loadConversations(openFirst=false) {
    try {
      const response=await fetch(`${API}/history/conversations`);
      if(!response.ok) throw new Error('History unavailable');
      const data=(await response.json()) as Conversation[];
      setConversations(data);
      if(openFirst&&data[0]) await openConversation(data[0].id);
    } catch { setConversations([]); }
  }

  async function openConversation(id:string) {
    const response=await fetch(`${API}/history/conversations/${id}`);
    if(!response.ok) return;
    const data=await response.json();
    setActiveId(data.id);setActiveTitle(data.title);
    const selectedMode=String(data.mode||'chat');
    setMode(selectedMode.charAt(0).toUpperCase()+selectedMode.slice(1));
    setMessages((data.messages||[]).map((item:{role:'user'|'assistant';content:string;image_data?:string})=>({role:item.role,text:item.content,imageData:item.image_data})));
    setMenu(false);
  }

  async function renameConversation(item:Conversation) {
    const title=window.prompt('Rename conversation',item.title)?.trim();
    if(!title)return;
    const response=await fetch(`${API}/history/conversations/${item.id}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({title})});
    if(response.ok){if(activeId===item.id)setActiveTitle(title);await loadConversations()}
  }

  async function deleteConversation(item:Conversation) {
    if(!window.confirm(`Delete "${item.title}"?`))return;
    const response=await fetch(`${API}/history/conversations/${item.id}`,{method:'DELETE'});
    if(response.ok){if(activeId===item.id)newChat();await loadConversations()}
  }

  async function selectFile(event: React.ChangeEvent<HTMLInputElement>) {
    const file=event.target.files?.[0];
    if(!file) return;
    const allowed=['text/','application/json','application/csv'];
    if(!allowed.some(type=>file.type.startsWith(type)) && !/\.(md|txt|csv|json|html|py|js|ts)$/i.test(file.name)){
      setMessages(v=>[...v,{role:'assistant',text:'This attachment control currently supports TXT, Markdown, CSV, JSON, HTML, and source-code files. PDF binary extraction is not connected yet.'}]);
      event.target.value=''; return;
    }
    const text=await file.text();
    setAttachment({name:file.name,text:text.slice(0,30000)});
    if(mode==='Chat') setMode('PDF');
    event.target.value='';
  }

  function startVoice() {
    const SpeechRecognition=(window as unknown as {SpeechRecognition?:new()=>any;webkitSpeechRecognition?:new()=>any}).SpeechRecognition
      ??(window as unknown as {webkitSpeechRecognition?:new()=>any}).webkitSpeechRecognition;
    if(!SpeechRecognition){setMessages(v=>[...v,{role:'assistant',text:'Voice input is not supported by this browser. Try the latest Chrome or Edge.'}]);return}
    const recognition=new SpeechRecognition();
    recognition.lang='en-IN'; recognition.interimResults=false; recognition.maxAlternatives=1;
    recognition.onstart=()=>setListening(true);
    recognition.onend=()=>setListening(false);
    recognition.onerror=()=>setListening(false);
    recognition.onresult=(event:any)=>setInput(v=>`${v}${v?' ':''}${event.results[0][0].transcript}`);
    recognition.start();
  }

  async function send() {
    const text=input.trim(); if(!text || loading) return;
    setMessages(v => [...v,{role:'user',text}]);
    setInput(''); setLoading(true);
    try {
      let conversationId=activeId;
      if(!conversationId){
        const title=text.length>44?`${text.slice(0,44)}...`:text;
        const created=await fetch(`${API}/history/conversations`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title,mode:mode.toLowerCase()})});
        if(!created.ok)throw new Error('Could not create conversation');
        const conversation=await created.json();conversationId=conversation.id;
        setActiveId(conversation.id);setActiveTitle(conversation.title);
      }
      await fetch(`${API}/history/conversations/${conversationId}/messages`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({role:'user',content:text})});
      const prompt=attachment?`${text}\n\nAttached file: ${attachment.name}\n---\n${attachment.text}`:text;
      const response=await fetch(`${API}/chat`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:prompt,provider:'openrouter',mode:mode.toLowerCase(),conversation_id:conversationId})});
      const data=await response.json(); if(!response.ok) throw new Error(data.detail??'Request failed');
      setMessages(v=>[...v,{role:'assistant',text:data.reply||'No response was returned.',imageData:data.image_data}]);
      await fetch(`${API}/history/conversations/${conversationId}/messages`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({role:'assistant',content:data.reply||'No response was returned.',image_data:data.image_data})});
      await loadConversations();
    } catch(error) {
      setMessages(v=>[...v,{role:'assistant',text:`I couldn’t reach OpenRouter. ${error instanceof Error?error.message:'Please try again.'}`}]);
    } finally { setLoading(false); setAttachment(null); }
  }
  function keyDown(event:KeyboardEvent<HTMLTextAreaElement>){if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();void send()}}
  function newChat(){setMessages([{role:'assistant',text:'Hello. How can I assist you today?'}]);setActiveId(null);setActiveTitle('New chat');setInput('');setAttachment(null);setMenu(false)}

  return <main className="app-shell">
    <aside className={`sidebar ${menu?'open':''}`}>
      <div className="brand-row"><button className="plain-icon" aria-label="Collapse sidebar" onClick={()=>setMenu(false)}><Icon name="panel"/></button><strong>NexoraAI</strong><span className="plan-badge">free</span><button className="plain-icon edit-button" aria-label="Compose new chat" onClick={newChat}><Icon name="edit"/></button></div>
      <button className="new-chat" onClick={newChat}><span>＋</span> New Chat</button>
      <div className="recent-section"><p className="section-label">RECENTS</p>{conversations.slice(0,8).map(item=><div key={item.id} className={`recent-item ${item.id===activeId?'active':''}`}><button className="recent-main" onClick={()=>void openConversation(item.id)}><span className="recent-icon"><Icon name="chat" size={17}/></span><span>{item.title}</span></button><button className="recent-action" aria-label={`Rename ${item.title}`} onClick={()=>void renameConversation(item)}><Icon name="edit" size={14}/></button><button className="recent-action danger" aria-label={`Delete ${item.title}`} onClick={()=>void deleteConversation(item)}><Icon name="trash" size={14}/></button></div>)}</div>
      <div className="profile-row"><div className="avatar">MS</div><div className="profile-copy"><strong>Mohit Sharma</strong><span>Free Plan</span></div><button className="gold-icon" aria-label="Invite link"><Icon name="link" size={18}/></button><button className="plain-icon" aria-label="Log out"><Icon name="logout" size={18}/></button></div>
    </aside>
    {menu&&<button className="sidebar-scrim" aria-label="Close sidebar" onClick={()=>setMenu(false)}/>}
    <section className="main-view">
      <header className="chat-header"><button className="plain-icon mobile-menu" aria-label="Open sidebar" onClick={()=>setMenu(true)}><Icon name="menu"/></button><span className="header-icon"><Icon name="chat"/></span><strong>{activeTitle}</strong><span className="message-count">{messages.length} Messages</span><div className="model-control"><span className={`status-dot ${ready?'ready':''}`}/><span className="selected-model">{modeModels[mode]}</span></div></header>
      <div className="conversation" ref={list}><div className="message-stack">{messages.map((item,index)=><div className={`message ${item.role}`} key={`${index}-${item.text}`}>{item.role==='assistant'&&messages.length>1&&<span className="assistant-mark">C</span>}<div className="message-content"><FormattedText text={item.text} copyable={item.role==='assistant'}/>{item.imageData&&<img className="generated-image" src={item.imageData} alt="AI generated result"/>}</div></div>)}{loading&&<div className="message assistant"><span className="assistant-mark">C</span><span className="typing"><i/><i/><i/></span></div>}</div></div>
      <footer className="composer-wrap">
        {ready===false&&<p className="setup-notice">Add <code>OPENROUTER_API_KEY</code> to the root <code>.env</code>, then restart the API.</p>}
        <div className="composer">
          <div className="mode-row">{modes.map(([label,icon])=><button key={label} className={`mode-pill ${label===mode?'active':''}`} onClick={()=>setMode(label)}><Icon name={icon} size={18}/>{label}</button>)}</div>
          {attachment&&<div className="attachment-chip"><Icon name="file" size={15}/><span>{attachment.name}</span><button aria-label="Remove attachment" onClick={()=>setAttachment(null)}>×</button></div>}
          <textarea value={input} onChange={e=>setInput(e.target.value)} onKeyDown={keyDown} placeholder="Chat with NexoraAI..." rows={2}/>
          <div className="composer-tools"><div>
            <input ref={fileInput} className="hidden-file" type="file" accept=".txt,.md,.csv,.json,.html,.py,.js,.ts,text/*" onChange={selectFile}/>
            <button className="tool-button" aria-label="Attach file" onClick={()=>fileInput.current?.click()}><Icon name="clip"/></button>
            <button className={`tool-button ${listening?'listening':''}`} aria-label="Voice input" onClick={startVoice}><Icon name="mic"/></button>
          </div><button className="send-button" aria-label="Send" disabled={!input.trim()||loading} onClick={()=>void send()}><Icon name="send" size={18}/></button></div>
        </div><p className="disclaimer">NexoraAI can make mistakes. Check important information.</p>
      </footer>
    </section>
  </main>;
}
