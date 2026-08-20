import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { predictionFormSchema, PredictionFormValues, SAMPLE_PRESET_CASES } from '../../schemas/predictionSchema';
import { Sparkles, Save, ArrowRight, Info, AlertCircle, RotateCcw } from 'lucide-react';

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
    setValue,
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

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-8">
      {/* Safe Sample Presets Selection */}
      <div className="card-glass p-5 border-blue-900/40 bg-blue-950/10">
        <div className="flex items-center space-x-2 mb-3">
          <Sparkles className="w-4 h-4 text-blue-400" />
          <h3 className="text-sm font-semibold text-blue-200">Load Filing Sample Presets</h3>
          <span className="text-[11px] text-slate-400">(Quickly test supported filing scenarios)</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {SAMPLE_PRESET_CASES.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleApplyPreset(idx)}
              className={`p-3 rounded-lg border text-left text-xs transition-all ${
                activePreset === preset.label
                  ? 'bg-blue-600/20 border-blue-500 text-blue-200 font-medium'
                  : 'bg-slate-800/60 border-slate-700/60 text-slate-300 hover:bg-slate-800 hover:border-slate-600'
              }`}
            >
              <div className="font-semibold mb-1 text-slate-200">{preset.label}</div>
              <div className="text-[11px] text-slate-400 leading-tight">{preset.description}</div>
            </button>
          ))}
        </div>
      </div>

      {/* SECTION 1: Case Basics & Geographical Identifiers */}
      <div className="card-glass p-6 space-y-4">
        <div className="border-b border-slate-800 pb-3 flex items-center justify-between">
          <div>
            <h3 className="text-base font-semibold text-slate-100">1. Case Identifiers & Geographical Codes</h3>
            <p className="text-xs text-slate-400">Required filing identifiers used for court establishment matching</p>
          </div>
          <span className="text-[11px] font-semibold text-rose-400 bg-rose-500/10 border border-rose-500/20 px-2 py-0.5 rounded">
            Required Fields Included
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              State Code <span className="text-rose-400">*</span>
            </label>
            <input
              type="text"
              {...register('state_code')}
              placeholder="e.g. 01"
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-blue-500 font-mono"
            />
            {errors.state_code && <p className="text-[11px] text-rose-400 mt-1">{errors.state_code.message}</p>}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              District Code <span className="text-rose-400">*</span>
            </label>
            <input
              type="text"
              {...register('dist_code')}
              placeholder="e.g. 01"
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-blue-500 font-mono"
            />
            {errors.dist_code && <p className="text-[11px] text-rose-400 mt-1">{errors.dist_code.message}</p>}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Court Number <span className="text-rose-400">*</span>
            </label>
            <input
              type="text"
              {...register('court_no')}
              placeholder="e.g. 01"
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-blue-500 font-mono"
            />
            {errors.court_no && <p className="text-[11px] text-rose-400 mt-1">{errors.court_no.message}</p>}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Type Name <span className="text-rose-400">*</span>
            </label>
            <input
              type="text"
              {...register('type_name')}
              placeholder="e.g. criminal appeal"
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-blue-500"
            />
            {errors.type_name && <p className="text-[11px] text-rose-400 mt-1">{errors.type_name.message}</p>}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">State Label</label>
            <input
              type="text"
              {...register('state_str')}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">District Label</label>
            <input
              type="text"
              {...register('district_str')}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Court Establishment Label</label>
            <input
              type="text"
              {...register('court_str')}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200"
            />
          </div>
        </div>
      </div>

      {/* SECTION 2: Case Classification & Temporal Attributes */}
      <div className="card-glass p-6 space-y-4">
        <div className="border-b border-slate-800 pb-3">
          <h3 className="text-base font-semibold text-slate-100">2. Case Classification & Filing Temporal Metadata</h3>
          <p className="text-xs text-slate-400">Case category, criminal flag, and filing calendar timing</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Filing Month (1-12)</label>
            <input
              type="number"
              min={1}
              max={12}
              {...register('filing_month')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100"
            />
            {errors.filing_month && <p className="text-[11px] text-rose-400 mt-1">{errors.filing_month.message}</p>}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Day of Week (0-6)</label>
            <input
              type="number"
              min={0}
              max={6}
              {...register('filing_day_of_week')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100"
            />
            {errors.filing_day_of_week && <p className="text-[11px] text-rose-400 mt-1">{errors.filing_day_of_week.message}</p>}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Filing Quarter (1-4)</label>
            <input
              type="number"
              min={1}
              max={4}
              {...register('filing_quarter')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100"
            />
            {errors.filing_quarter && <p className="text-[11px] text-rose-400 mt-1">{errors.filing_quarter.message}</p>}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Case Category</label>
            <select
              {...register('case_category')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100"
            >
              <option value="criminal">Criminal</option>
              <option value="civil">Civil</option>
              <option value="commercial">Commercial</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Case Type Standard</label>
            <input
              type="text"
              {...register('case_type_str')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Is Criminal Code</label>
            <select
              {...register('is_criminal_code')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono"
            >
              <option value={1}>1 (Yes - Criminal)</option>
              <option value={0}>0 (No - Civil/Other)</option>
            </select>
          </div>
        </div>
      </div>

      {/* SECTION 3: Statutory Acts & Demographics */}
      <div className="card-glass p-6 space-y-4">
        <div className="border-b border-slate-800 pb-3">
          <h3 className="text-base font-semibold text-slate-100">3. Statutory Provisions & Legal Representation</h3>
          <p className="text-xs text-slate-400">Act counts, section counts, bailable status, and gender indicators</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Statutory Act Count</label>
            <input
              type="number"
              min={0}
              {...register('statutory_act_count')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">IPC Section Count</label>
            <input
              type="number"
              min={0}
              {...register('ipc_section_count')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Bailable IPC Flag</label>
            <select
              {...register('bailable_ipc_flag')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100"
            >
              <option value="bailable">Bailable</option>
              <option value="non-bailable">Non-Bailable</option>
              <option value="unknown">Unknown / N/A</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Primary Act ID</label>
            <input
              type="text"
              {...register('primary_act_id')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Female Defendant</label>
            <select
              {...register('female_defendant_clean')}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200"
            >
              <option value="0">0 (No / Unknown)</option>
              <option value="1">1 (Yes)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Female Petitioner</label>
            <select
              {...register('female_petitioner_clean')}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200"
            >
              <option value="0">0 (No / Unknown)</option>
              <option value="1">1 (Yes)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Female Defense Counsel</label>
            <select
              {...register('female_adv_def_clean')}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200"
            >
              <option value="0">0 (No / Unknown)</option>
              <option value="1">1 (Yes)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Female Petitioner Counsel</label>
            <select
              {...register('female_adv_pet_clean')}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200"
            >
              <option value="0">0 (No / Unknown)</option>
              <option value="1">1 (Yes)</option>
            </select>
          </div>
        </div>
      </div>

      {/* SECTION 4: Judicial Attributes & Prior Historical Metrics */}
      <div className="card-glass p-6 space-y-4">
        <div className="border-b border-slate-800 pb-3">
          <h3 className="text-base font-semibold text-slate-100">4. Judicial Assignment & Historical Court Throughput</h3>
          <p className="text-xs text-slate-400">Judge attributes and baseline historical administrative metrics</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Filing Judge ID</label>
            <input
              type="text"
              {...register('ddl_filing_judge_id')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Judge Position</label>
            <input
              type="text"
              {...register('judge_position_clean')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Judge Gender</label>
            <select
              {...register('judge_gender')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100"
            >
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="unknown">Unknown</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Judge Tenure Days</label>
            <input
              type="number"
              min={0}
              {...register('judge_tenure_days')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Court Prior Delay Rate (0.0-1.0)</label>
            <input
              type="number"
              step="0.01"
              min={0}
              max={1}
              {...register('court_prior_delay_rate')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Court Prior Avg Duration (Days)</label>
            <input
              type="number"
              step="1"
              min={0}
              {...register('court_prior_avg_duration')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Court Prior Active Backlog</label>
            <input
              type="number"
              step="1"
              min={0}
              {...register('court_prior_active_backlog')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Case Type Delay Rate (0.0-1.0)</label>
            <input
              type="number"
              step="0.01"
              min={0}
              max={1}
              {...register('casetype_prior_delay_rate')}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono"
            />
          </div>
        </div>
      </div>

      {/* Form Submission Toolbar */}
      <div className="card-glass p-5 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-3 text-xs text-slate-300">
          <label className="flex items-center space-x-2 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={saveAsCase}
              onChange={(e) => setSaveAsCase(e.target.checked)}
              className="w-4 h-4 rounded bg-slate-900 border-slate-700 text-blue-600 focus:ring-blue-500"
            />
            <span className="font-semibold text-slate-200">Save Case Record to Repository</span>
          </label>
          <span className="text-slate-500">|</span>
          <span className="text-slate-400">Submits case features to live FastAPI ML serving pipeline</span>
        </div>

        <div className="flex items-center space-x-3 w-full md:w-auto">
          <button
            type="button"
            onClick={() => reset(SAMPLE_PRESET_CASES[0].values)}
            className="flex-1 md:flex-none inline-flex items-center justify-center space-x-2 bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2.5 rounded-lg text-xs font-semibold transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset</span>
          </button>

          <button
            type="submit"
            disabled={isSubmitting}
            className="flex-1 md:flex-none inline-flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white px-6 py-2.5 rounded-lg text-xs font-semibold shadow-lg shadow-blue-500/25 transition-all"
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
