export type BlockType = "warmup" | "work" | "recovery" | "cooldown" | "ramp";

export interface WorkoutBlock {
  id: string;
  type: BlockType;
  duration: number;
  intensity: number;
  isEditing: boolean;
  startPower: number;
  endPower: number;
  groupId?: string;
}

export interface BlockGroup {
  id: string;
  blocks: string[];
  repeats: number;
}

export interface Workout {
  blocks: WorkoutBlock[];
  groups: BlockGroup[];
  totalDuration: number;
}
