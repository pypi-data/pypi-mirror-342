import React from "react";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { Trash2, GripVertical, Edit2, Check } from "lucide-react";
import { WorkoutBlock as WorkoutBlockType, BlockGroup } from "../types/workout";

interface WorkoutBlockProps {
  block: WorkoutBlockType;
  onUpdate: (updates: Partial<WorkoutBlockType>) => void;
  onDelete: () => void;
  isSelected: boolean;
  onSelect: () => void;
  group?: BlockGroup;
}

export const WorkoutBlock: React.FC<WorkoutBlockProps> = ({
  block,
  onUpdate,
  onDelete,
  isSelected,
  onSelect,
  group,
}) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: block.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    zIndex: isDragging ? 1 : undefined,
    position: isDragging ? "relative" : undefined,
  };

  const types = ["warmup", "work", "recovery", "cooldown", "ramp"];
  const colors = {
    warmup: {
      bg: "bg-blue-50",
      border: "border-blue-200",
      text: "text-blue-700",
      bar: "bg-blue-200",
    },
    work: {
      bg: "bg-red-50",
      border: "border-red-200",
      text: "text-red-700",
      bar: "bg-red-200",
    },
    recovery: {
      bg: "bg-green-50",
      border: "border-green-200",
      text: "text-green-700",
      bar: "bg-green-200",
    },
    cooldown: {
      bg: "bg-purple-50",
      border: "border-purple-200",
      text: "text-purple-700",
      bar: "bg-purple-200",
    },
    ramp: {
      bg: "bg-yellow-50",
      border: "border-yellow-200",
      text: "text-yellow-700",
      bar: "bg-yellow-200",
    },
  };

  const color = colors[block.type];

  const handleBlockClick = (e: React.MouseEvent) => {
    const target = e.target as HTMLElement;
    const isInteractive =
      target.closest("button") ||
      target.closest("input") ||
      target.closest("select");
    if (!isInteractive) {
      onSelect();
    }
  };

  const handleDoneClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    onUpdate({ isEditing: false });
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`rounded-lg border ${color.bg} ${color.border} overflow-hidden shadow-sm ${
        isDragging ? "shadow-lg" : ""
      } ${isSelected ? "ring-2 ring-blue-400" : ""}`}
      onClick={handleBlockClick}
    >
      {block.isEditing ? (
        <div className="p-3" onClick={(e) => e.stopPropagation()}>
          <div className="grid grid-cols-4 gap-3">
            <select
              value={block.type}
              onChange={(e) =>
                onUpdate({ type: e.target.value as WorkoutBlockType["type"] })
              }
              className="bg-white rounded px-2 py-1.5 text-sm border border-gray-200"
            >
              {types.map((type) => (
                <option key={type} value={type}>
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </option>
              ))}
            </select>

            <div className="flex items-center gap-1">
              <input
                type="number"
                value={block.duration}
                onChange={(e) =>
                  onUpdate({
                    duration: Math.max(1, parseInt(e.target.value)),
                  })
                }
                className="w-full px-2 py-1.5 rounded border border-gray-200 text-sm"
                min="1"
              />
              <span className="text-xs text-gray-500">s</span>
            </div>

            {block.type === "ramp" ? (
              <>
                <div className="flex items-center gap-1">
                  <input
                    type="number"
                    value={block.startPower || 0}
                    onChange={(e) =>
                      onUpdate({
                        startPower: Math.max(0, parseInt(e.target.value)),
                      })
                    }
                    className="w-full px-2 py-1.5 rounded border border-gray-200 text-sm"
                    min="0"
                  />
                  <span className="text-xs text-gray-500">Start Watt</span>
                </div>
                <div className="flex items-center gap-1">
                  <input
                    type="number"
                    value={block.endPower || 0}
                    onChange={(e) =>
                      onUpdate({
                        endPower: Math.max(0, parseInt(e.target.value)),
                      })
                    }
                    className="w-full px-2 py-1.5 rounded border border-gray-200 text-sm"
                    min="0"
                  />
                  <span className="text-xs text-gray-500">End Watt</span>
                </div>
              </>
            ) : (
              <div className="flex items-center gap-1">
                <input
                  type="number"
                  value={block.intensity}
                  onChange={(e) =>
                    onUpdate({
                      intensity: Math.min(
                        3000,
                        Math.max(0, parseInt(e.target.value))
                      ),
                    })
                  }
                  className="w-full px-2 py-1.5 rounded border border-gray-200 text-sm"
                  min="0"
                  max="3000"
                />
                <span className="text-xs text-gray-500">Watt</span>
              </div>
            )}
          </div>
          <button
            onClick={handleDoneClick}
            className={`mt-2 flex items-center gap-1 text-sm ${color.text} font-medium`}
          >
            <Check size={14} />
            Done
          </button>
        </div>
      ) : (
        <div className="relative">
          <div className="absolute left-0 bottom-0 h-1 w-full bg-gray-100">
            <div
              className={`h-full ${color.bar} transition-all duration-200`}
              style={{ width: `${block.intensity || block.startPower || 0}%` }}
            />
          </div>
          <div className="p-3 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                className="touch-none cursor-grab active:cursor-grabbing"
                {...attributes}
                {...listeners}
              >
                <GripVertical className="w-4 h-4 text-gray-400" />
              </button>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-medium capitalize">{block.type}</span>
                </div>
                <div className="text-sm text-gray-600">
                  {block.type === "ramp"
                    ? `${block.duration}s from ${block.startPower || 0}W to ${
                        block.endPower || 0
                      }W`
                    : `${block.duration}s @ ${block.intensity} Watt`}
                </div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onUpdate({ isEditing: true });
                }}
                className="p-1 text-gray-500 hover:text-gray-700 transition-colors"
              >
                <Edit2 size={16} />
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete();
                }}
                className="p-1 text-gray-500 hover:text-red-600 transition-colors"
              >
                <Trash2 size={16} />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
