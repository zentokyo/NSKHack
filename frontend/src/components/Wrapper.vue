<template>
    <div class="w-full flex flex-col items-center">
        <header class="fixed top-0 w-full bg-stone-800 p-6 flex justify-between">
            <h1 class=" text-4xl text-white font-medium">Заголовок</h1>
            <button @click="console.log('оператор запрошен')" class="px-4 py-2 bg-stone-700 rounded-2xl text-white">Вызов оператора</button>
        </header>
        <main class="pt-30 pb-50 min-h-screen w-full px-60 overflow-y-clip">
            <Messages />
        </main>
        <footer class="fixed bottom-0 inset-x-0">
            <Inputer />
        </footer>
    </div>
</template>

<script setup>
import Inputer from './Inputer.vue';
import Messages from './Messages.vue';


</script>

<style scoped>

</style>