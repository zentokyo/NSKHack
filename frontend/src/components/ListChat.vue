<template>
    <div class="p-2">
        <h1 class="text-white font-bold text-2xl py-4 text-center">Список чатов</h1>
        <div class="w-full h-0.5 bg-stone-600"></div>
        <div class="w-full flex justify-center">
            <button @click="messagesStore.createChat" class=" mt-4 text-white bg-violet-600 hover:bg-violet-500 active:bg-violet-400 py-2 px-4 rounded-2xl h-min">
                Создать чат
            </button>
        </div>
        <ul class="mt-4 flex flex-col gap-4">
            <li @click="messagesStore.selectChat(chat.chat_id)" v-for="chat in messagesStore.chatList" :key="chat.chat_id" class="py-2 px-4 bg-stone-600 hover:bg-stone-500 active:bg-stone-400 rounded-2xl text-white">
                {{chat.title}}
            </li>
        </ul>    
    </div>
</template>

<script setup>
import { useMessagesStore } from '@/stores/messages';
import { onMounted } from 'vue';

const messagesStore = useMessagesStore();


onMounted(() => {
    messagesStore.getChatList();
})
</script>

<style lang="scss" scoped></style>
