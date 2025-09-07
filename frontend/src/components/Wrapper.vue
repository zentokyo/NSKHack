<template>
    <div class="w-full flex flex-col items-center relative">
        <div class="overflow-y-scroll fixed z-20 h-screen left-0 w-100 h-full pb-6 bg-stone-700 transition-transform duration-300 ease-in-out"
        :class="[isOpen ? 'translate-x-0' : '-translate-x-full']">
            <ListChat />
        </div>
        <div @click="isOpen = false" v-show="isOpen" class="absolute z-10 inset-0 bg-stone-900/60"></div>
        
        <header class="fixed top-0 w-full bg-stone-800 p-6 flex justify-between">    
            <button @click="isOpen = !isOpen" class="py-2 px-3 bg-stone-700 rounded-2xl text-white hover:bg-stone-600 active:bg-stone-500 font-black ">|||</button>
            <h1 class=" text-4xl text-white font-medium">{{ messageStore.thisChat.title }}</h1>
            <button @click="callOperator" class="px-4 py-2 bg-stone-700 rounded-2xl text-white hover:bg-stone-600 active:bg-stone-500">Вызов оператора</button>
        </header>
        <main class="pt-30 pb-50 min-h-screen w-full px-60 overflow-y-auto">
            <Messages />
        </main>
        <footer class="fixed bottom-0 inset-x-0">
            <Inputer />
        </footer>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import Inputer from './Inputer.vue';
import Messages from './Messages.vue';
import ListChat from './ListChat.vue';
import { useMessagesStore } from '@/stores/messages';

const messageStore = useMessagesStore();

const isOpen = ref(false);

const callOperator = () => {
    console.log('Оператор запрошен');
}


</script>

<style scoped>

</style>