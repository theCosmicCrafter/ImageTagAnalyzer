import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Image Tag Analyzer header', () => {
  render(<App />);
  const headerElement = screen.getByText(/Image Tag Analyzer/i);
  expect(headerElement).toBeInTheDocument();
});
