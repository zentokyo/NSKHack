<template>
  <div class="p-5 bg-stone-800 flex justify-center">
    <button v-if="messagesStore.isNewChat" @click="messagesStore.createChat" class=" mt-4 text-white bg-violet-600 hover:bg-violet-500 active:bg-violet-400 py-2 px-4 rounded-2xl h-min">
      Создать чат
    </button>
    <div v-else class="flex flex-row items-center justify-center gap-4">
      <textarea
        :disabled="messagesStore.loading"
        name="inputPromt"
        v-model="inputPromt"
        placeholder="Введите запрос"
        class="bg-stone-700 outline-0 w-150 resize-none px-5 py-4 rounded-2xl text-white disabled:opacity-50 disabled:cursor-not-allowed"
        @keydown="handleKeydown"
      ></textarea>
      <button @click="sendMessage" class="text-white bg-violet-600 hover:bg-violet-500 active:bg-violet-400 py-2 px-4 rounded-2xl h-min">
        Отправить
      </button>
    </div>
  </div>
</template>

<script setup>
import { useMessagesStore } from '@/stores/messages';
import { ref } from 'vue';

const messagesStore  = useMessagesStore();

const inputPromt = ref('');


const sendMessage = () => {
  if (inputPromt.value.trim() === '') return;

  messagesStore.sendMessage(inputPromt.value);
  inputPromt.value = '';
};

const handleKeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
};
</script>

<style lang="scss" scoped></style>
