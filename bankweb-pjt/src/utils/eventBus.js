// src/utils/eventBus.js
import { defineEmits } from 'vue'
import mitt from 'mitt'

export const emitter = mitt()