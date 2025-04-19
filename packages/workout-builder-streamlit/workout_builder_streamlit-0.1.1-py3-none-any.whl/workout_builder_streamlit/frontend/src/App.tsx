import React, { useState, useEffect } from "react";
import { Timer, Activity, Link2, Unlink } from "lucide-react";
import {
  DndContext,
  DragEndEvent,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { WorkoutBlock } from "./components/WorkoutBlock";
import type {
  Workout,
  WorkoutBlock as WorkoutBlockType,
  BlockGroup,
} from "./types/workout";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";

function App(props: any) {
  const [workout, setWorkout] = useState<Workout>({
    blocks: [],
    groups: [],
    totalDuration: 0,
  });

  useEffect(() => {
    Streamlit.setComponentValue(workout);
    Streamlit.setFrameHeight();
  }, [workout]);

  const [selectedBlocks, setSelectedBlocks] = useState<string[]>([]);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    }),
  );

  const addBlock = () => {
    setWorkout((prev) => ({
      ...prev,
      blocks: [
        ...prev.blocks,
        {
          id: `block-${Date.now()}`,
          type: "work",
          duration: 120,
          intensity: 140,
          repeats: 1,
          isEditing: false,
          startPower: 0,
          endPower: 0,
        },
      ],
    }));
  };

  const updateBlock = (blockId: string, updates: Partial<WorkoutBlockType>) => {
    setWorkout((prev) => ({
      ...prev,
      blocks: prev.blocks.map((block) =>
        block.id === blockId ? { ...block, ...updates } : block,
      ),
    }));
  };

  const deleteBlock = (blockId: string) => {
    setWorkout((prev) => {
      const newGroups = prev.groups
        .map((group) => ({
          ...group,
          blocks: group.blocks.filter((id) => id !== blockId),
        }))
        .filter((group) => group.blocks.length > 1);

      return {
        ...prev,
        blocks: prev.blocks.filter((block) => block.id !== blockId),
        groups: newGroups,
      };
    });
    setSelectedBlocks((prev) => prev.filter((id) => id !== blockId));
  };

  const toggleBlockSelection = (blockId: string) => {
    setSelectedBlocks((prev) => {
      if (prev.includes(blockId)) {
        return prev.filter((id) => id !== blockId);
      }

      const blockIndex = workout.blocks.findIndex(
        (block) => block.id === blockId,
      );

      if (prev.length === 0) {
        return [blockId];
      }

      const selectedIndices = prev.map((id) =>
        workout.blocks.findIndex((block) => block.id === id),
      );

      const isAdjacent = selectedIndices.some(
        (index) => Math.abs(index - blockIndex) === 1,
      );

      if (!isAdjacent) {
        return [blockId];
      }

      return [...prev, blockId];
    });
  };

  const groupBlocks = () => {
    if (selectedBlocks.length < 2) return;

    const sortedBlocks = selectedBlocks.sort((a, b) => {
      const indexA = workout.blocks.findIndex((block) => block.id === a);
      const indexB = workout.blocks.findIndex((block) => block.id === b);
      return indexA - indexB;
    });

    const indices = sortedBlocks.map((id) =>
      workout.blocks.findIndex((block) => block.id === id),
    );

    const isConsecutive = indices.every(
      (index, i) => i === 0 || index === indices[i - 1] + 1,
    );

    if (!isConsecutive) {
      setSelectedBlocks([]);
      return;
    }

    const groupId = `group-${Date.now()}`;
    setWorkout((prev) => ({
      ...prev,
      groups: [
        ...prev.groups,
        {
          id: groupId,
          blocks: sortedBlocks,
          repeats: 1,
        },
      ],
    }));
    setSelectedBlocks([]);
  };

  const ungroupBlocks = (groupId: string) => {
    setWorkout((prev) => ({
      ...prev,
      groups: prev.groups.filter((group) => group.id !== groupId),
    }));
  };

  const updateGroupRepeats = (groupId: string, repeats: number) => {
    setWorkout((prev) => ({
      ...prev,
      groups: prev.groups.map((group) =>
        group.id === groupId ? { ...group, repeats } : group,
      ),
    }));
  };

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      setWorkout((prev) => {
        const oldIndex = prev.blocks.findIndex(
          (block) => block.id === active.id,
        );
        const newIndex = prev.blocks.findIndex((block) => block.id === over.id);

        return {
          ...prev,
          blocks: arrayMove(prev.blocks, oldIndex, newIndex),
        };
      });
    }
  };

  const getBlockGroup = (blockId: string): BlockGroup | undefined => {
    return workout.groups.find((group) => group.blocks.includes(blockId));
  };

  const totalDuration = workout.blocks.reduce((total, block) => {
    const group = getBlockGroup(block.id);
    return total + block.duration * (group ? group.repeats : 1);
  }, 0);

  return (
    <div className="max-w-2xl mx-auto p-4">
      <header className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2 text-gray-600 bg-white px-4 py-2 rounded-lg shadow-sm">
          <Timer className="w-5 h-5" />
          <span className="font-medium">
            {Math.floor(totalDuration / 60)} min
          </span>
        </div>
      </header>

      <div className="flex justify-end mb-4">
        {selectedBlocks.length >= 2 ? (
          <button
            onClick={groupBlocks}
            className="flex items-center gap-1 px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors text-sm font-medium"
          >
            <Link2 size={16} />
            Group Selected ({selectedBlocks.length})
          </button>
        ) : null}
      </div>

      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <SortableContext
          items={workout.blocks}
          strategy={verticalListSortingStrategy}
        >
          <div className="space-y-3">
            {workout.blocks.map((block) => {
              // Check if the block belongs to a group
              const group = workout.groups.find((group) =>
                group.blocks.includes(block.id),
              );

              // If the block is part of a group and it's the first block in the group, render the entire group
              if (group && group.blocks[0] === block.id) {
                const groupBlocks = group.blocks
                  .map((blockId) =>
                    workout.blocks.find((b) => b.id === blockId),
                  )
                  .filter(Boolean); // Filter out any null values

                return (
                  <div
                    key={group.id}
                    className="relative px-4 pt-10 bg-blue-50 border border-blue-200 rounded-lg"
                  >
                    {/* Group Controls */}
                    <div className="absolute top-0 left-0 p-2 flex items-center gap-2">
                      <label className="text-sm text-gray-600">repeats:</label>
                      <input
                        type="number"
                        value={group.repeats || 1}
                        onChange={(e) =>
                          updateGroupRepeats(
                            group.id,
                            Math.max(1, parseInt(e.target.value) || 1),
                          )
                        }
                        className="w-12 px-1 py-1 rounded border border-gray-200 text-sm"
                        min="1"
                      />
                      <button
                        onClick={() => ungroupBlocks(group.id)}
                        className="text-red-500 hover:text-red-700"
                        aria-label="Ungroup Blocks"
                      >
                        <Unlink size={16} />
                      </button>
                    </div>
                    {groupBlocks.map((groupBlock) => (
                      <div key={groupBlock!.id} className="py-1">
                        <WorkoutBlock
                          block={groupBlock!}
                          onUpdate={(updates) =>
                            updateBlock(groupBlock!.id, updates)
                          }
                          onDelete={() => deleteBlock(groupBlock!.id)}
                          isSelected={selectedBlocks.includes(groupBlock!.id)}
                          onSelect={() =>
                            toggleBlockSelection(groupBlock!.id)
                          }
                          group={group}
                        />
                      </div>
                    ))}
                  </div>
                );
              }

              // If the block is not part of a group, render it as a single block
              if (!group) {
                return (
                  <div key={block.id} className="relative">
                    <WorkoutBlock
                      block={block}
                      onUpdate={(updates) => updateBlock(block.id, updates)}
                      onDelete={() => deleteBlock(block.id)}
                      isSelected={selectedBlocks.includes(block.id)}
                      onSelect={() => toggleBlockSelection(block.id)}
                    />
                  </div>
                );
              }

              // Skip rendering for blocks that are part of a group but not the first block
              return null;
            })}
          </div>
        </SortableContext>
      </DndContext>

      <button
        onClick={addBlock}
        className="mt-4 w-full py-3 px-4 bg-blue-50 border-2 border-dashed border-blue-200 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors text-sm font-medium"
      >
        + Add Interval
      </button>
    </div>
  );
}

// export default App;
export default withStreamlitConnection(App);
