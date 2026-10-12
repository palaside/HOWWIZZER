// src/shims/fs.ts
// Minimal shim for Node's 'fs' module to avoid Vite/CJS attempts to lstat the root drive.
// All exported functions are no-ops; they satisfy imports but do nothing.
export const lstat = () => {};
export const stat = () => {};
export const readFile = () => {};
export const writeFile = () => {};
export const unlink = () => {};
export const readdir = () => {};
export const mkdir = () => {};
export const rmdir = () => {};
export const existsSync = () => false;
