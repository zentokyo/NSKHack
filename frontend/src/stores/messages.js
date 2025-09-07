import { defineStore } from 'pinia'

// let idMessage = 0

export const useMessagesStore = defineStore('messages', {
  state: () => ({
    // messages: [],
    loading: false,
    error: null,

    chatList: {},

    thisChat: {},

    isNewChat: true,
  }),
  actions: {
    
    async selectChat(id){
      
      try{
        const response = await fetch(`http://localhost:8000/chats/${id}`, {
          method: 'GET',
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.thisChat = data;
        this.isNewChat = false;
        console.log(this.thisChat);
      }catch (error) {
        console.error('Ошибка при отправке сообщения:', error);
        this.error = error.message;
      }
    },
    async getChatList() {
      try{
        const response = await fetch('http://localhost:8000/chats', {
          method: 'GET',});

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.chatList = data;
        // console.log(this.chatList);
      }catch (error) {
        console.error('Ошибка при отправке сообщения:', error);
        this.error = error.message;
      }
    },
    // addMessage(message) {
    //   const newMessage = {
    //     id: idMessage++,
    //     rating: message.sender === 'bot' ? 3 : undefined,
    //     ...message
    //   };
    //   this.messages.push(newMessage);
    // },

    async createChat() {
      console.log('create chat');
      try{
        const response = await fetch('http://localhost:8000/chats', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ title: 'New chat' })
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.thisChat = data;
        console.log(this.thisChat);
      }catch (error) {
        console.error('Ошибка при отправке сообщения:', error);
        this.error = error.message;
        this.addMessage({ text: "Извините, произошла ошибка при обработке вашего запроса", 
          sender: 'bot' });
      }

      this.isNewChat = false;
    },

    async sendMessage(text) {
      const message = { text: text, sender: 'user' };

      this.loading = true;
      this.error = null;

      try{
        const response = await fetch(`http://localhost:8000/chats/${this.thisChat.chat_id}/messages`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(message)
        });
        // console.log(message);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("logdata response for send", data);
        this.selectChat(this.thisChat.chat_id);
      }catch (error) {
        console.error('Ошибка при отправке сообщения:', error);
        this.error = error.message;
      }finally{this.loading = false;}
      console.log(this.messages);
    },

    // async sendMessage(text){
    //   const message = { text: text, sender: 'user' };
    //   this.addMessage(message);
      
    //   this.loading = true;
    //   this.error = null;

    //   try {
    //     // Отправляем запрос на сервер FastAPI с помощью fetch
    //     const response = await fetch('http://localhost:8000/messages', {
    //       method: 'POST',
    //       headers: {
    //         'Content-Type': 'application/json'
    //       },
    //       body: JSON.stringify({ text: text })
    //     });
    //     if (!response.ok) {
    //       throw new Error(`HTTP error! status: ${response.status}`);
    //     }
    //     const data = await response.json();
    //     // console.log(data);
        
    //     this.addMessage({text: data, sender: 'bot'});
    //   } catch (error) {
    //     console.error('Ошибка при отправке сообщения:', error);
    //     this.error = error.message;
    //     this.addMessage({ text: "Извините, произошла ошибка при обработке вашего запроса", 
    //       sender: 'bot' });
    //   }finally{this.loading = false;}
    //   console.log(this.messages);
        
    //   },
    changeRating(id, grade){
      if (this.messages[id].sender === 'bot') {
        if (this.messages[id].rating === grade){
          this.messages[id].rating = 3;
          return;
        }
        this.messages[id].rating = grade;
      }
    }
  }
})