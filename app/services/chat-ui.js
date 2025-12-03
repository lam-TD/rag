class CompanyChat extends HTMLElement {
  static get observedAttributes() {
    return ['api-url', 'project-id', 'title', 'subtitle', 'placeholder', 'theme', 'adapter'];
  }

  constructor() {
    super();

    this.messages = [];
    this.isSending = false;
    this._initialized = false;

    this.apiUrl = this.getAttribute('api-url') || '';
    this.projectId = this.getAttribute('project-id') || '';
    this.widgetTitle = this.getAttribute('title') || 'Company AI Assistant';
    this.widgetSubtitle = this.getAttribute('subtitle') || '';
    this.placeholder = this.getAttribute('placeholder') || 'Send a message...';
    this.theme = this.getAttribute('theme') || 'dark';
    this.adapterName = this.getAttribute('adapter') || null;
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue === newValue) return;
    switch (name) {
      case 'api-url':
        this.apiUrl = newValue;
        break;
      case 'project-id':
        this.projectId = newValue;
        break;
      case 'title':
        this.widgetTitle = newValue || 'Company AI Assistant';
        break;
      case 'subtitle':
        this.widgetSubtitle = newValue || '';
        break;
      case 'placeholder':
        this.placeholder = newValue || 'Send a message...';
        break;
      case 'theme':
        this.theme = newValue || 'dark';
        break;
      case 'adapter':
        this.adapterName = newValue || null;
        break;
    }

    if (this._initialized) {
      this.renderBase();
      this.renderAllMessages();
    }
  }

  connectedCallback() {
    this.renderBase();
    this._initialized = true;
  }

  renderBase() {
    const themeClass = this.theme === 'light' ? 'cc-theme-light' : 'cc-theme-dark';

    const html = `
      <div class="cc-app ${themeClass}">
        <div class="cc-header">
          <div class="cc-header-logo">AI</div>
          <div class="cc-header-text">
            <div class="cc-header-title">${this.escapeHtml(this.widgetTitle)}</div>
            <div class="cc-header-subtitle">${this.escapeHtml(this.widgetSubtitle)}</div>
          </div>
        </div>

        <div class="cc-body">
          <div class="cc-messages-wrapper">
            <div class="cc-messages"></div>
          </div>
          <div class="cc-typing" hidden>
            <span>Assistant is thinking</span>
            <div class="cc-typing-dots">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>

        <div class="cc-footer">
          <div class="cc-input-wrapper">
            <form class="cc-input-row">
              <div class="cc-textarea-wrapper">
                <textarea
                  class="cc-input"
                  rows="1"
                  placeholder="${this.escapeHtml(this.placeholder)}"
                ></textarea>
                <button class="cc-send-btn" type="submit">
                  <span>Send</span>
                  <span>↵</span>
                </button>
              </div>
            </form>
            <div class="cc-hint">
              AI có thể trả lời về tài liệu nội bộ, quy trình, hướng dẫn... Đừng nhập thông tin nhạy cảm.
            </div>
          </div>
        </div>
      </div>
    `;

    this.innerHTML = html;

    this.appRoot = this.querySelector('.cc-app');
    this.messagesWrapperEl = this.querySelector('.cc-messages-wrapper');
    this.messagesEl = this.querySelector('.cc-messages');
    this.typingEl = this.querySelector('.cc-typing');
    this.textarea = this.querySelector('.cc-input');
    this.sendBtn = this.querySelector('.cc-send-btn');
    this.form = this.querySelector('.cc-input-row');

    this.bindEvents();
  }

  bindEvents() {
    if (!this.form || !this.textarea) return;

    this.form.addEventListener('submit', (e) => {
      e.preventDefault();
      this.handleSend();
    });

    this.textarea.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.handleSend();
      } else {
        // auto resize
        this.autoResizeTextarea();
      }
    });

    this.textarea.addEventListener('input', () => {
      this.autoResizeTextarea();
    });
  }

  async handleSend() {
    const text = (this.textarea.value || '').trim();
    if (!text || this.isSending) return;

    this.addMessage({ role: 'user', content: text });
    this.textarea.value = '';
    this.autoResizeTextarea();
    this.setSending(true);

    this.dispatchEvent(new CustomEvent('chat:send', {
      detail: { role: 'user', content: text, messages: this.messages },
      bubbles: true
    }));

    try {
      const response = await this.sendToBackend();
      const answer = (response && response.answer) || 'Không nhận được câu trả lời.';
      const sources = Array.isArray(response && response.sources) ? response.sources : [];

      this.addMessage({ role: 'assistant', content: answer, sources });

      this.dispatchEvent(new CustomEvent('chat:response', {
        detail: { answer, sources, raw: response },
        bubbles: true
      }));
    } catch (err) {
      console.error('RAG error:', err);
      this.addMessage({
        role: 'assistant',
        content: 'Xin lỗi, hệ thống đang gặp lỗi. Vui lòng thử lại sau.'
      });

      this.dispatchEvent(new CustomEvent('chat:error', {
        detail: { error: err },
        bubbles: true
      }));
    } finally {
      this.setSending(false);
    }
  }

  async sendToBackend() {
    const payload = {
      project_id: this.projectId || undefined,
      messages: this.messages.map((m) => ({ role: m.role, content: m.content }))
    };

    // adapter custom
    if (this.adapterName && typeof window[this.adapterName] === 'function') {
      return await window[this.adapterName]({
        messages: payload.messages,
        projectId: payload.project_id,
        widget: this
      });
    }

    // fetch mặc định
    if (!this.apiUrl) {
      throw new Error('company-chat: api-url is required if no adapter is provided');
    }

    const res = await fetch(this.apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const text = await res.text().catch(() => '');
      throw new Error(`RAG API error: ${res.status} ${text}`);
    }

    return await res.json();
  }

  setSending(isSending) {
    this.isSending = isSending;
    if (this.sendBtn) this.sendBtn.disabled = isSending;
    if (this.typingEl) this.typingEl.hidden = !isSending;
  }

  addMessage(msg) {
    this.messages.push({
      role: msg.role,
      content: msg.content,
      sources: msg.sources || []
    });
    this.renderMessage(msg);
    this.scrollToBottom();
  }

  renderAllMessages() {
    if (!this.messagesEl) return;
    this.messagesEl.innerHTML = '';
    this.messages.forEach((msg) => this.renderMessage(msg));
    this.scrollToBottom();
  }

  renderMessage(msg) {
    if (!this.messagesEl) return;

    const item = document.createElement('div');
    item.className = `cc-message cc-role-${msg.role}`;

    const avatar = document.createElement('div');
    avatar.className = 'cc-avatar';
    avatar.textContent = msg.role === 'user' ? 'You' : 'AI';

    const bubble = document.createElement('div');
    bubble.className = 'cc-bubble';

    const content = document.createElement('div');
    content.className = 'cc-content';
    content.textContent = msg.content;
    bubble.appendChild(content);

    if (msg.role === 'assistant' && msg.sources && msg.sources.length) {
      const sourcesEl = document.createElement('div');
      sourcesEl.className = 'cc-sources';
      msg.sources.forEach((s, idx) => {
        const srcItem = document.createElement('div');
        srcItem.className = 'cc-source-item';
        srcItem.textContent = `[${idx + 1}] ${s.title || 'Nguồn tham khảo'}`;
        if (s.url) {
          srcItem.addEventListener('click', () => window.open(s.url, '_blank'));
        }
        sourcesEl.appendChild(srcItem);
      });
      bubble.appendChild(sourcesEl);
    }

    item.appendChild(avatar);
    item.appendChild(bubble);
    this.messagesEl.appendChild(item);
  }

  scrollToBottom() {
    if (!this.messagesWrapperEl) return;
    this.messagesWrapperEl.scrollTop = this.messagesWrapperEl.scrollHeight;
  }

  autoResizeTextarea() {
    if (!this.textarea) return;
    this.textarea.style.height = 'auto';
    this.textarea.style.height = this.textarea.scrollHeight + 'px';
  }

  escapeHtml(str) {
    if (str == null) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  // public methods cho app bên ngoài
  clear() {
    this.messages = [];
    if (this.messagesEl) this.messagesEl.innerHTML = '';
  }

  addSystemMessage(text) {
    this.addMessage({ role: 'assistant', content: text, sources: [] });
  }
}

if (!customElements.get('company-chat')) {
  customElements.define('company-chat', CompanyChat);
}