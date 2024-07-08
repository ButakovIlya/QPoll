import { Box } from '@mui/material';
import { DragDropContext, Draggable, Droppable } from 'react-beautiful-dnd';

import { DragWrapper } from './styled';

const DraggableList = ({ renderItem, items, onDragEnd, pollType, disabled = false }) => {
  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <Droppable droppableId="options">
        {(provided) => (
          <Box {...provided.droppableProps} ref={provided.innerRef}>
            {items?.map((item, index) => (
              <Draggable
                key={item.id}
                draggableId={item.id.toString()}
                index={index}
                isDragDisabled={item.is_free_response || disabled}
              >
                {(provided) => (
                  <DragWrapper
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...(!item.is_free_response ? provided.dragHandleProps : {})}
                    pollType={pollType}
                    style={{
                      ...provided.draggableProps.style,
                      cursor: item.isDraggable ? 'grab' : 'default',
                    }}
                  >
                    {renderItem(item, index)}
                  </DragWrapper>
                )}
              </Draggable>
            ))}
            {provided.placeholder}
          </Box>
        )}
      </Droppable>
    </DragDropContext>
  );
};

export default DraggableList;
