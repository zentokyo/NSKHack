<template>
  <div class="flex flex-row items-center justify-center gap-4 p-5 bg-stone-800">
    <textarea
      name="inputPromt"
      v-model="inputPromt"
      placeholder="Введите запрос"
      class="bg-stone-700 outline-0 w-150 resize-none px-5 py-4 rounded-2xl text-white"
      @keydown="handleKeydown"
    ></textarea>
    <button @click="sendMessage" class="text-white bg-violet-600 py-2 px-4 rounded-2xl h-min">
      Отправить
    </button>
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
