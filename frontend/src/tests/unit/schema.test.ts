import { describe, it, expect } from 'vitest';
import { predictionFormSchema, SAMPLE_PRESET_CASES } from '../../schemas/predictionSchema';

describe('Prediction Form Zod Schema Validation', () => {
  it('should validate a complete valid filing feature preset', () => {
    const preset = SAMPLE_PRESET_CASES[0].values;
    const result = predictionFormSchema.safeParse(preset);
    expect(result.success).toBe(true);
  });

  it('should fail validation when required fields are missing', () => {
    const invalidPayload = {
      ...SAMPLE_PRESET_CASES[0].values,
      state_code: '',
      type_name: '',
    };
    const result = predictionFormSchema.safeParse(invalidPayload);
    expect(result.success).toBe(false);
    if (!result.success) {
      const fieldErrors = result.error.flatten().fieldErrors;
      expect(fieldErrors.state_code).toBeDefined();
      expect(fieldErrors.type_name).toBeDefined();
    }
  });

  it('should enforce month range bounds (1 to 12)', () => {
    const invalidMonth = {
      ...SAMPLE_PRESET_CASES[0].values,
      filing_month: 13,
    };
    const result = predictionFormSchema.safeParse(invalidMonth);
    expect(result.success).toBe(false);
  });

  it('should enforce delay rate bounds between 0.0 and 1.0', () => {
    const invalidRate = {
      ...SAMPLE_PRESET_CASES[0].values,
      court_prior_delay_rate: 1.5,
    };
    const result = predictionFormSchema.safeParse(invalidRate);
    expect(result.success).toBe(false);
  });
});
