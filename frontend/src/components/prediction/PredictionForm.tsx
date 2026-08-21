import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { predictionFormSchema, PredictionFormValues, SAMPLE_PRESET_CASES } from '../../schemas/predictionSchema';
import { Sparkles, ArrowRight, RotateCcw } from 'lucide-react';

interface PredictionFormProps {
  onSubmit: (values: PredictionFormValues, saveAsCase: boolean) => Promise<void>;
  isSubmitting?: boolean;
}

export const PredictionForm: React.FC<PredictionFormProps> = ({ onSubmit, isSubmitting = false }) => {
  const [saveAsCase, setSaveAsCase] = useState<boolean>(true);
  const [activePreset, setActivePreset] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<PredictionFormValues>({
    resolver: zodResolver(predictionFormSchema),
    defaultValues: SAMPLE_PRESET_CASES[0].values,
  });

  const handleApplyPreset = (index: number) => {
    const preset = SAMPLE_PRESET_CASES[index];
    reset(preset.values);
    setActivePreset(preset.label);
  };

  const handleFormSubmit = async (values: PredictionFormValues) => {
    await onSubmit(values, saveAsCase);
  };

  const inputClass = "w-full bg-surface-container-lowest border border-outline-variant rounded-md px-3 py-2 text-on-surface font-body-md focus:outline-none focus:border-secondary focus:ring-1 focus:ring-secondary transition-shadow";
  const labelClass = "block font-label-md text-label-md text-on-surface-variant mb-1";
  const sectionClass = "bg-surface-container-lowest border border-outline-variant/50 rounded-lg shadow-sm p-6 space-y-4";
  const headerClass = "font-headline-sm text-headline-sm text-primary";
  const subheadClass = "font-body-md text-body-md text-on-surface-variant mt-1";

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-stack-md">
      {/* Safe Sample Presets Selection */}
      <div className="bg-primary-container/5 border border-primary-container/20 rounded-lg p-5">
        <div className="flex items-center space-x-2 mb-3">
          <Sparkles className="w-4 h-4 text-primary" />
          <h3 className="font-label-md text-label-md text-primary">Load Filing Sample Presets</h3>
          <span className="font-label-sm text-label-sm text-on-surface-variant">(Quickly test supported filing scenarios)</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {SAMPLE_PRESET_CASES.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleApplyPreset(idx)}
              className={`p-3 rounded-lg border text-left transition-all ${
                activePreset === preset.label
                  ? 'bg-primary-container/10 border-primary text-primary'
                  : 'bg-surface-container-lowest border-outline-variant/50 text-on-surface hover:bg-surface-container-low hover:border-outline'
              }`}
            >
              <div className="font-label-md text-label-md mb-1">{preset.label}</div>
              <div className="font-label-sm text-label-sm text-on-surface-variant leading-tight">{preset.description}</div>
            </button>
          ))}
        </div>
      </div>

      {/* SECTION 1: Case Basics & Geographical Identifiers */}
      <div className={sectionClass}>
        <div className="border-b border-outline-variant pb-3 flex items-center justify-between">
          <div>
            <h3 className={headerClass}>1. Case Identifiers & Geographical Codes</h3>
            <p className={subheadClass}>Required filing identifiers used for court establishment matching</p>
          </div>
          <span className="font-label-sm text-label-sm text-error bg-error-container border border-error/20 px-2 py-0.5 rounded">
            Required Fields Included
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className={labelClass}>
              State Code <span className="text-error">*</span>
            </label>
            <input
              type="text"
              {...register('state_code')}
              placeholder="e.g. 01"
              className={`${inputClass} font-data-mono`}
            />
            {errors.state_code && <p className="font-label-sm text-label-sm text-error mt-1">{errors.state_code.message}</p>}
          </div>

          <div>
            <label className={labelClass}>
              District Code <span className="text-error">*</span>
            </label>
            <input
              type="text"
              {...register('dist_code')}
              placeholder="e.g. 01"
              className={`${inputClass} font-data-mono`}
            />
            {errors.dist_code && <p className="font-label-sm text-label-sm text-error mt-1">{errors.dist_code.message}</p>}
          </div>

          <div>
            <label className={labelClass}>
              Court Number <span className="text-error">*</span>
            </label>
            <input
              type="text"
              {...register('court_no')}
              placeholder="e.g. 01"
              className={`${inputClass} font-data-mono`}
            />
            {errors.court_no && <p className="font-label-sm text-label-sm text-error mt-1">{errors.court_no.message}</p>}
          </div>

          <div>
            <label className={labelClass}>
              Type Name <span className="text-error">*</span>
            </label>
            <input
              type="text"
              {...register('type_name')}
              placeholder="e.g. criminal appeal"
              className={inputClass}
            />
            {errors.type_name && <p className="font-label-sm text-label-sm text-error mt-1">{errors.type_name.message}</p>}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          <div>
            <label className={labelClass}>State Label</label>
            <input type="text" {...register('state_str')} className={inputClass} />
          </div>
          <div>
            <label className={labelClass}>District Label</label>
            <input type="text" {...register('district_str')} className={inputClass} />
          </div>
          <div>
            <label className={labelClass}>Court Establishment Label</label>
            <input type="text" {...register('court_str')} className={inputClass} />
          </div>
        </div>
      </div>

      {/* SECTION 2: Case Classification & Temporal Attributes */}
      <div className={sectionClass}>
        <div className="border-b border-outline-variant pb-3">
          <h3 className={headerClass}>2. Case Classification & Filing Temporal Metadata</h3>
          <p className={subheadClass}>Case category, criminal flag, and filing calendar timing</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div>
            <label className={labelClass}>Filing Month (1-12)</label>
            <input type="number" min={1} max={12} {...register('filing_month')} className={inputClass} />
            {errors.filing_month && <p className="font-label-sm text-label-sm text-error mt-1">{errors.filing_month.message}</p>}
          </div>

          <div>
            <label className={labelClass}>Day of Week (0-6)</label>
            <input type="number" min={0} max={6} {...register('filing_day_of_week')} className={inputClass} />
            {errors.filing_day_of_week && <p className="font-label-sm text-label-sm text-error mt-1">{errors.filing_day_of_week.message}</p>}
          </div>

          <div>
            <label className={labelClass}>Filing Quarter (1-4)</label>
            <input type="number" min={1} max={4} {...register('filing_quarter')} className={inputClass} />
            {errors.filing_quarter && <p className="font-label-sm text-label-sm text-error mt-1">{errors.filing_quarter.message}</p>}
          </div>

          <div>
            <label className={labelClass}>Case Category</label>
            <select {...register('case_category')} className={inputClass}>
              <option value="criminal">Criminal</option>
              <option value="civil">Civil</option>
              <option value="commercial">Commercial</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div>
            <label className={labelClass}>Case Type Standard</label>
            <input type="text" {...register('case_type_str')} className={inputClass} />
          </div>

          <div>
            <label className={labelClass}>Is Criminal Code</label>
            <select {...register('is_criminal_code')} className={`${inputClass} font-data-mono`}>
              <option value={1}>1 (Yes - Criminal)</option>
              <option value={0}>0 (No - Civil/Other)</option>
            </select>
          </div>
        </div>
      </div>

      {/* SECTION 3: Statutory Acts & Demographics */}
      <div className={sectionClass}>
        <div className="border-b border-outline-variant pb-3">
          <h3 className={headerClass}>3. Statutory Provisions & Legal Representation</h3>
          <p className={subheadClass}>Act counts, section counts, bailable status, and gender indicators</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className={labelClass}>Statutory Act Count</label>
            <input type="number" min={0} {...register('statutory_act_count')} className={inputClass} />
          </div>

          <div>
            <label className={labelClass}>IPC Section Count</label>
            <input type="number" min={0} {...register('ipc_section_count')} className={inputClass} />
          </div>

          <div>
            <label className={labelClass}>Bailable IPC Flag</label>
            <select {...register('bailable_ipc_flag')} className={inputClass}>
              <option value="bailable">Bailable</option>
              <option value="non-bailable">Non-Bailable</option>
              <option value="unknown">Unknown / N/A</option>
            </select>
          </div>

          <div>
            <label className={labelClass}>Primary Act ID</label>
            <input type="text" {...register('primary_act_id')} className={`${inputClass} font-data-mono`} />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2">
          <div>
            <label className={labelClass}>Female Defendant</label>
            <select {...register('female_defendant_clean')} className={inputClass}>
              <option value="0">0 (No / Unknown)</option>
              <option value="1">1 (Yes)</option>
            </select>
          </div>

          <div>
            <label className={labelClass}>Female Petitioner</label>
            <select {...register('female_petitioner_clean')} className={inputClass}>
              <option value="0">0 (No / Unknown)</option>
              <option value="1">1 (Yes)</option>
            </select>
          </div>

          <div>
            <label className={labelClass}>Female Defense Counsel</label>
            <select {...register('female_adv_def_clean')} className={inputClass}>
              <option value="0">0 (No / Unknown)</option>
              <option value="1">1 (Yes)</option>
            </select>
          </div>

          <div>
            <label className={labelClass}>Female Petitioner Counsel</label>
            <select {...register('female_adv_pet_clean')} className={inputClass}>
              <option value="0">0 (No / Unknown)</option>
              <option value="1">1 (Yes)</option>
            </select>
          </div>
        </div>
      </div>

      {/* SECTION 4: Judicial Attributes & Prior Historical Metrics */}
      <div className={sectionClass}>
        <div className="border-b border-outline-variant pb-3">
          <h3 className={headerClass}>4. Judicial Assignment & Historical Court Throughput</h3>
          <p className={subheadClass}>Judge attributes and baseline historical administrative metrics</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className={labelClass}>Filing Judge ID</label>
            <input type="text" {...register('ddl_filing_judge_id')} className={`${inputClass} font-data-mono`} />
          </div>

          <div>
            <label className={labelClass}>Judge Position</label>
            <input type="text" {...register('judge_position_clean')} className={inputClass} />
          </div>

          <div>
            <label className={labelClass}>Judge Gender</label>
            <select {...register('judge_gender')} className={inputClass}>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="unknown">Unknown</option>
            </select>
          </div>

          <div>
            <label className={labelClass}>Judge Tenure Days</label>
            <input type="number" min={0} {...register('judge_tenure_days')} className={inputClass} />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
          <div>
            <label className={labelClass}>Court Prior Delay Rate (0.0-1.0)</label>
            <input type="number" step="0.01" min={0} max={1} {...register('court_prior_delay_rate')} className={`${inputClass} font-data-mono`} />
          </div>

          <div>
            <label className={labelClass}>Court Prior Avg Duration (Days)</label>
            <input type="number" step="1" min={0} {...register('court_prior_avg_duration')} className={`${inputClass} font-data-mono`} />
          </div>

          <div>
            <label className={labelClass}>Court Prior Active Backlog</label>
            <input type="number" step="1" min={0} {...register('court_prior_active_backlog')} className={`${inputClass} font-data-mono`} />
          </div>

          <div>
            <label className={labelClass}>Case Type Delay Rate (0.0-1.0)</label>
            <input type="number" step="0.01" min={0} max={1} {...register('casetype_prior_delay_rate')} className={`${inputClass} font-data-mono`} />
          </div>
        </div>
      </div>

      {/* Form Submission Toolbar */}
      <div className="bg-surface-container-low border border-outline-variant/50 p-5 rounded-lg flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-2 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={saveAsCase}
              onChange={(e) => setSaveAsCase(e.target.checked)}
              className="w-4 h-4 rounded border-outline text-primary focus:ring-primary"
            />
            <span className="font-label-md text-label-md text-on-surface">Save Case Record to Repository</span>
          </label>
          <span className="text-outline-variant">|</span>
          <span className="font-label-sm text-label-sm text-on-surface-variant">Submits case features to live FastAPI ML serving pipeline</span>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <button
            type="button"
            onClick={() => reset(SAMPLE_PRESET_CASES[0].values)}
            className="flex-1 md:flex-none inline-flex items-center justify-center gap-2 bg-surface-container-highest hover:bg-outline-variant text-on-surface px-4 py-2.5 rounded-md font-label-md transition-colors"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Reset</span>
          </button>

          <button
            type="submit"
            disabled={isSubmitting}
            className="flex-1 md:flex-none inline-flex items-center justify-center gap-2 bg-primary hover:bg-primary-container text-on-primary disabled:opacity-50 px-6 py-2.5 rounded-md font-label-md transition-all shadow-sm"
          >
            {isSubmitting ? (
              <span>Executing ML Inference...</span>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Run Filing Risk Evaluation</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>
    </form>
  );
};
