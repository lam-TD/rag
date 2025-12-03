class RagChatWidget extends HTMLElement {
  static get observedAttributes() {
    return ['api-url', 'project-id', 'title', 'subtitle', 'placeholder', 'theme', 'adapter'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.messages = [];
    this.isSending = false;

    // cached config
    this.apiUrl = this.getAttribute('api-url') || '';
    this.projectId = this.getAttribute('project-id') || '';
    this.widgetTitle = this.getAttribute('title') || 'AI Assistant';
    this.widgetSubtitle = this.getAttribute('subtitle') || '';
    this.placeholder = this.getAttribute('placeholder') || 'Nhập câu hỏi của bạn...';
    this.theme = this.getAttribute('theme') || 'light';
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
        this.widgetTitle = newValue || 'AI Assistant';
        break;
      case 'subtitle':
        this.widgetSubtitle = newValue || '';
        break;
      case 'placeholder':
        this.placeholder = newValue || 'Nhập câu hỏi của bạn...';
        break;
      case 'theme':
        this.theme = newValue || 'light';
        break;
      case 'adapter':
        this.adapterName = newValue || null;
        break;
    }
    // re-render header / input nếu đã mount
    if (this._initialized) {
      this.renderBase(); // render lại khung, message vẫn giữ
      this.renderAllMessages();
    }
  }

  connectedCallback() {
    this.renderBase();
    this._initialized = true;
  }

  renderBase() {
    const themeClass = this.theme === 'dark' ? 'rcw-theme-dark' : '';

    const style = `
      :host {
        display: block;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      }
      .rcw-chat {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        max-width: 420px;
        height: 520px;
        background: #ffffff;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        font-size: 13px;
      }
      .rcw-chat.rcw-theme-dark {
        background: #111827;
        color: #f9fafb;
        border-color: #1f2937;
      }

      .rcw-header {
        padding: 10px 14px;
        border-bottom: 1px solid #e5e7eb;
        background: linear-gradient(120deg, #2563eb, #4f46e5);
        color: #fff;
      }
      .rcw-title {
        font-weight: 600;
        font-size: 14px;
      }
      .rcw-subtitle {
        font-size: 11px;
        opacity: 0.9;
        margin-top: 2px;
      }

      .rcw-messages {
        flex: 1;
        padding: 10px 10px 0;
        overflow-y: auto;
        background: #f9fafb;
      }
      .rcw-chat.rcw-theme-dark .rcw-messages {
        background: #020617;
      }

      .rcw-message {
        display: flex;
        margin-bottom: 10px;
        gap: 8px;
      }
      .rcw-message--user {
        flex-direction: row-reverse;
      }
      .rcw-avatar {
        width: 24px;
        height: 24px;
        border-radius: 999px;
        font-size: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #2563eb;
        color: #fff;
        flex-shrink: 0;
      }
      .rcw-message--assistant .rcw-avatar {
        background: #4b5563;
      }

      .rcw-bubble {
        max-width: 80%;
        padding: 8px 10px;
        border-radius: 12px;
        line-height: 1.4;
        white-space: pre-wrap;
        word-wrap: break-word;
      }
      .rcw-message--assistant .rcw-bubble {
        background: #ffffff;
        border: 1px solid #e5e7eb;
      }
      .rcw-message--user .rcw-bubble {
        background: #2563eb;
        color: #fff;
      }

      .rcw-chat.rcw-theme-dark .rcw-message--assistant .rcw-bubble {
        background: #111827;
        border-color: #1f2937;
        color: #e5e7eb;
      }
      .rcw-chat.rcw-theme-dark .rcw-message--user .rcw-bubble {
        background: #2563eb;
      }

      .rcw-sources {
        margin-top: 6px;
        font-size: 11px;
        color: #6b7280;
      }
      .rcw-source-item {
        cursor: pointer;
        text-decoration: underline;
      }

      .rcw-input-row {
        display: flex;
        padding: 8px;
        border-top: 1px solid #e5e7eb;
        background: #f9fafb;
        gap: 8px;
      }
      .rcw-input {
        flex: 1;
        resize: none;
        border-radius: 8px;
        border: 1px solid #d1d5db;
        padding: 6px 8px;
        font-size: 13px;
        max-height: 96px;
        min-height: 32px;
      }
      .rcw-input:focus {
        outline: none;
        border-color: #2563eb;
        box-shadow: 0 0 0 1px rgba(37,99,235,0.3);
      }
      .rcw-send-btn {
        border: none;
        border-radius: 999px;
        padding: 0 14px;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        background: #2563eb;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 60px;
      }
      .rcw-send-btn[disabled] {
        opacity: 0.6;
        cursor: default;
      }
      .rcw-footer-hint {
        font-size: 10px;
        text-align: right;
        padding: 0 10px 6px;
        color: #9ca3af;
      }
      .rcw-chat.rcw-theme-dark .rcw-footer-hint {
        color: #6b7280;
      }
    `;

    const html = `
      <div class="rcw-chat ${themeClass}">
        <div class="rcw-header">
          <div class="rcw-title">${this.escapeHtml(this.widgetTitle)}</div>
          <div class="rcw-subtitle">${this.escapeHtml(this.widgetSubtitle)}</div>
        </div>
        <div class="rcw-messages"></div>
        <form class="rcw-input-row">
          <textarea class="rcw-input" rows="1" placeholder="${this.escapeHtml(this.placeholder)}"></textarea>
          <button class="rcw-send-btn" type="submit">Gửi</button>
        </form>
        <div class="rcw-footer-hint">Powered by Company RAG</div>
      </div>
    `;

    this.shadowRoot.innerHTML = `
      <style>${style}</style>
      ${html}
    `;

    this.chatRoot = this.shadowRoot.querySelector('.rcw-chat');
    this.messagesEl = this.shadowRoot.querySelector('.rcw-messages');
    this.textarea = this.shadowRoot.querySelector('.rcw-input');
    this.sendBtn = this.shadowRoot.querySelector('.rcw-send-btn');
    this.form = this.shadowRoot.querySelector('.rcw-input-row');

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
      }
    });
  }

  async handleSend() {
    const text = (this.textarea.value || '').trim();
    if (!text || this.isSending) return;

    this.addMessage({ role: 'user', content: text });
    this.textarea.value = '';
    this.setSending(true);

    // phát event cho app bên ngoài nếu muốn hook
    this.dispatchEvent(new CustomEvent('rag:send', {
      detail: { role: 'user', content: text, messages: this.messages },
      bubbles: true
    }));

    try {
      const response = await this.sendToBackend();
      const answer = (response && response.answer) || 'Không nhận được câu trả lời.';
      const sources = Array.isArray(response && response.sources) ? response.sources : [];

      this.addMessage({ role: 'assistant', content: answer, sources });

      this.dispatchEvent(new CustomEvent('rag:response', {
        detail: { answer, sources, raw: response },
        bubbles: true
      }));
    } catch (err) {
      console.error('RAG error:', err);
      this.addMessage({
        role: 'assistant',
        content: 'Xin lỗi, hệ thống đang gặp lỗi. Vui lòng thử lại sau.'
      });

      this.dispatchEvent(new CustomEvent('rag:error', {
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

    // 1. Nếu có adapter, gọi adapter
    if (this.adapterName && typeof window[this.adapterName] === 'function') {
      return await window[this.adapterName]({
        messages: payload.messages,
        projectId: payload.project_id,
        widget: this
      });
    }

    // 2. Nếu không có adapter, dùng fetch mặc định
    if (!this.apiUrl) {
      throw new Error('rag-chat-widget: api-url is required if no adapter is provided');
    }

    const res = await fetch(this.apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
        // có thể thêm Authorization ở đây nếu cần
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
    if (this.sendBtn) {
      this.sendBtn.disabled = isSending;
    }
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
    item.className = `rcw-message rcw-message--${msg.role}`;

    const avatar = document.createElement('div');
    avatar.className = 'rcw-avatar';
    avatar.textContent = msg.role === 'user' ? 'Y' : 'A';

    const bubble = document.createElement('div');
    bubble.className = 'rcw-bubble';

    const content = document.createElement('div');
    content.className = 'rcw-content';
    content.textContent = msg.content;
    bubble.appendChild(content);

    if (msg.role === 'assistant' && msg.sources && msg.sources.length) {
      const sourcesEl = document.createElement('div');
      sourcesEl.className = 'rcw-sources';
      msg.sources.forEach((s, idx) => {
        const srcItem = document.createElement('div');
        srcItem.className = 'rcw-source-item';
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
    if (!this.messagesEl) return;
    this.messagesEl.scrollTop = this.messagesEl.scrollHeight;
  }

  // helper tránh XSS nếu truyền trực tiếp từ attribute
  escapeHtml(str) {
    if (str == null) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  // --- public methods cho app bên ngoài nếu cần ---
  clear() {
    this.messages = [];
    if (this.messagesEl) this.messagesEl.innerHTML = '';
  }

  addSystemMessage(text) {
    this.addMessage({ role: 'assistant', content: text, sources: [] });
  }
}

if (!customElements.get('rag-chat-widget')) {
  customElements.define('rag-chat-widget', RagChatWidget);
}