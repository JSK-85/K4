import { useEffect, useRef, useState } from 'react';

export interface PersistenceState {
  status: 'saved' | 'error';
  error: string;
}

interface PersistentStateOptions<T> {
  validate?: (value: unknown) => value is T;
  mergeExternal?: (local: T, external: T) => T;
  maxBytes?: number;
}

export function usePersistentState<T>(
  key: string,
  initialValue: T,
  options: PersistentStateOptions<T> = {},
) {
  const optionsRef = useRef(options);
  optionsRef.current = options;
  const [initialRead] = useState(() => {
    try {
      const stored = window.localStorage.getItem(key);
      if (!stored) return { value: initialValue, error: '' };
      const parsed: unknown = JSON.parse(stored);
      if (options.validate && !options.validate(parsed)) {
        return {
          value: initialValue,
          error: `Stored data for ${key} failed validation and was left untouched.`,
        };
      }
      return { value: parsed as T, error: '' };
    } catch (error) {
      return {
        value: initialValue,
        error: `Could not read ${key}: ${error instanceof Error ? error.message : 'unknown error'}`,
      };
    }
  });
  const [value, setValue] = useState<T>(initialRead.value);
  const [persistence, setPersistence] = useState<PersistenceState>({
    status: initialRead.error ? 'error' : 'saved',
    error: initialRead.error,
  });
  const invalidStoredValue = useRef(Boolean(initialRead.error));

  useEffect(() => {
    if (invalidStoredValue.current) return;
    try {
      const serialized = JSON.stringify(value);
      const maxBytes = optionsRef.current.maxBytes ?? 4_500_000;
      if (new Blob([serialized]).size > maxBytes) {
        throw new Error(`data exceeds the ${Math.round(maxBytes / 1_000_000)} MB safety limit`);
      }
      window.localStorage.setItem(key, serialized);
      setPersistence({ status: 'saved', error: '' });
    } catch (error) {
      setPersistence({
        status: 'error',
        error: `Could not save ${key}: ${error instanceof Error ? error.message : 'unknown error'}`,
      });
    }
  }, [key, value]);

  useEffect(() => {
    const synchronize = (event: StorageEvent) => {
      if (event.key !== key || event.newValue === null) return;
      try {
        const parsed: unknown = JSON.parse(event.newValue);
        if (optionsRef.current.validate && !optionsRef.current.validate(parsed)) {
          throw new Error('external data failed validation');
        }
        invalidStoredValue.current = false;
        setPersistence({ status: 'saved', error: '' });
        setValue((current) =>
          optionsRef.current.mergeExternal
            ? optionsRef.current.mergeExternal(current, parsed as T)
            : (parsed as T),
        );
      } catch (error) {
        setPersistence({
          status: 'error',
          error: `Could not synchronize ${key}: ${error instanceof Error ? error.message : 'unknown error'}`,
        });
      }
    };
    window.addEventListener('storage', synchronize);
    return () => window.removeEventListener('storage', synchronize);
  }, [key]);

  const resetStoredValue = () => {
    try {
      const serialized = JSON.stringify(initialValue);
      window.localStorage.setItem(key, serialized);
      invalidStoredValue.current = false;
      setValue(initialValue);
      setPersistence({ status: 'saved', error: '' });
    } catch (error) {
      setPersistence({
        status: 'error',
        error: `Could not reset ${key}: ${error instanceof Error ? error.message : 'unknown error'}`,
      });
    }
  };

  return [value, setValue, persistence, resetStoredValue] as const;
}
