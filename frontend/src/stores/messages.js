import { defineStore } from 'pinia'

let idMessage = 0

export const useMessagesStore = defineStore('messages', {
  state: () => ({
    messages: [
      // { text: "first", sender: 'user' },
      // { text: "654", sender: 'bot', rating: 5},{ text: "123", sender: 'user' },
      // { text: "654lefjk sejkr gjdsfgkj; dsf;gkl jdsflk;g dslk;fgj dskl;jg kl;dsfjg ;lksdfjglk dsjg lk;dsfjgkl; sdjfgkl; dsfjgk; dsfjkl ", sender: 'bot' },{ text: "123", sender: 'user' },
      // { text: "654", sender: 'bot', rating: 1 },{ text: "654lefjk sejkr gjdsfgkj; dsf;gkl jdsflk;g dslk;fgj dskl;jg kl;dsfjg ;lksdfjglk dsjg lk;dsfjgkl; sdjfgkl; dsfjgk; dsfjkl ", sender: 'user' },
      // { text: "last", sender: 'bot' }, 
    ],
    loading: false,
    error: null,


  // messages: [

  // ]
  }),
  actions: {
    addMessage(message) {
      const newMessage = {
        id: idMessage++,
        rating: message.sender === 'bot' ? 3 : undefined,
        ...message
      };
      this.messages.push(newMessage);
    },

    async sendMessage(text){
      const message = { text: text, sender: 'user' };
      this.addMessage(message);
      
      this.loading = true;
      this.error = null;

      try {
        // Отправляем запрос на сервер FastAPI с помощью fetch
        const response = await fetch('http://localhost:8000/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: text })
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // console.log(data);
        
        this.addMessage({text: data, sender: 'bot'});
      } catch (error) {
        console.error('Ошибка при отправке сообщения:', error);
        this.error = error.message;
        this.addMessage({ text: "Извините, произошла ошибка при обработке вашего запроса", 
          sender: 'bot' });
      }finally{this.loading = false;}
      console.log(this.messages);
        
      },
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