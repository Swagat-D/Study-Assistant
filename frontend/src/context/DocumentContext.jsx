import { createContext } from 'react';

export const DocumentContext = createContext({
  documents: [],
  setDocuments: () => {},
  activeDocument: null,
  setActiveDocument: () => {},
});