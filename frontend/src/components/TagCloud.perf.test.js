import React from 'react';
import { render } from '@testing-library/react';
import TagCloud from './TagCloud';

describe('TagCloud Performance', () => {
    it('measures render performance with large list', () => {
        // Generate a large list of tags
        const generateTags = (count) => {
            return Array.from({ length: count }, (_, i) => ({
                tag_name: `tag-${i}`,
                confidence: Math.random() * 100,
                is_primary: i === 0
            }));
        };

        const initialTags = generateTags(5000);
        // Prepend an item
        const updatedTags = [{
            tag_name: 'new-tag',
            confidence: 95,
            is_primary: false // make sure it's not primary to avoid confusion with existing primary
        }, ...initialTags];

        // Measure initial render
        const startRender = performance.now();
        const { rerender } = render(<TagCloud tags={initialTags} />);
        const endRender = performance.now();
        console.log(`Initial render time: ${(endRender - startRender).toFixed(2)}ms`);

        // Measure update
        const startUpdate = performance.now();
        rerender(<TagCloud tags={updatedTags} />);
        const endUpdate = performance.now();
        console.log(`Update render time: ${(endUpdate - startUpdate).toFixed(2)}ms`);
    });
});
