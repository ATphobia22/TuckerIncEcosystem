// Copied from ATphobia22/Quantum-Studio-1.0/types.ts
// Source revision: fabd68e35c9c15067e55a85aceb6568451f43240
// Retained as a bounded UI/type reference; not wired into the Python runtime.

export enum AIModel {
  FLASH = 'gemini-3-flash-preview',
  PRO = 'gemini-3-pro-preview',
  LITE = 'gemini-flash-lite-latest',
  IMAGE = 'gemini-2.5-flash-image',
  TTS = 'gemini-2.5-flash-preview-tts'
}

export interface GroundingSource {
  title: string;
  uri: string;
}

export interface Message {
  id: string;
  role: 'user' | 'model' | 'system';
  content: string;
  imageUrl?: string;
  sources?: GroundingSource[];
  timestamp: number;
  isStreaming?: boolean;
}

export type ToolCategory = 'Quantum' | 'Developer' | 'AI' | 'OS' | 'FinTech' | 'Enterprise';

export interface QuantumTool {
  id: string;
  name: string;
  provider: string;
  description: string;
  icon: string;
  isActive: boolean;
  category: ToolCategory;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  model: AIModel;
  updatedAt: number;
}

export interface QuantumState {
  hasOnboarded: boolean;
  currentSessionId: string | null;
  sessions: ChatSession[];
  activeToolIds: string[];
}
