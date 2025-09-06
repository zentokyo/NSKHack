<template>
  <div class="flex flex-col gap-4">
    <div
      v-for="message in messagesStore.messages"
      :key="message.id"
      :class="[
        'flex',
        message.sender === 'user' ? 'justify-end' : 'justify-start',
      ]"
    >
      <div class="flex flex-col gap-1">
        <div
          :class="[
            'px-5 py-4 rounded-2xl max-w-xs',
            message.sender === 'user'
              ? 'bg-violet-600 text-white'
              : 'bg-stone-700 text-white',
          ]"
        >
          {{ message.text }}
        </div>
        <div v-if="message.sender === 'bot'" class="flex justify-end gap-2">
          <button @click="messagesStore.changeRating(message.id, 5)" :class="['p-2',
            message.rating === 5
              ? 'bg-stone-700 rounded-full'
							: '',
          ]">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="25"
              height="25"
              viewBox="0 0 26 26"
              fill="white"
            >
              <path
                fill="white"
                d="M17.869 3.889c-2.096 0-3.887 1.494-4.871 2.524c-.984-1.03-2.771-2.524-4.866-2.524C4.521 3.889 2 6.406 2 10.009c0 3.97 3.131 6.536 6.16 9.018c1.43 1.173 2.91 2.385 4.045 3.729c.191.225.471.355.765.355h.058c.295 0 .574-.131.764-.355c1.137-1.344 2.616-2.557 4.047-3.729C20.867 16.546 24 13.98 24 10.009c0-3.603-2.521-6.12-6.131-6.12z"
              />
            </svg>
          </button>

          <button @click="messagesStore.changeRating(message.id, 1)" :class="[
						'p-2',
            message.rating === 1
              ? 'bg-stone-700 p-2 rounded-full'
							: '',
          ]">
          	<svg
	            xmlns="http://www.w3.org/2000/svg"
	            width="25"
	            height="25"
	            viewBox="0 0 24 24"
	          >
	            <path
	              fill="white"
	              d="m2.808 1.394l18.384 18.384l-1.414 1.415l-3.746-3.747L12 21.486l-8.478-8.493a6 6 0 0 1 .033-8.023L1.394 2.808l1.414-1.414Zm2.172 10.23l7.02 7.03l2.618-2.622l-9.646-9.646a4 4 0 0 0 .008 5.237Zm15.263-6.866a6 6 0 0 1 .236 8.235l-1.635 1.636l-1.414-1.414l1.59-1.592a4 4 0 0 0-5.683-5.606l-1.335 1.198l-1.336-1.197a3.975 3.975 0 0 0-1.155-.723l-2.25-2.25A5.99 5.99 0 0 1 12 4.53a5.998 5.998 0 0 1 8.242.229Z"
	            />
	          </svg>
          </button>
        </div>
      </div>
    </div>
		<div v-if="messagesStore.loading" class="text-white">loader...</div>
  </div>
</template>

<script setup>
import { useMessagesStore } from "@/stores/messages";

const messagesStore = useMessagesStore();
</script>

<style lang="scss" scoped></style>
