import React from 'react';
import { Briefcase, MapPin, Calendar, Building } from 'lucide-react';
import { resolveMediaUrl } from '@/lib/media';

const ExperienceSection = ({ experience }) => {
    if (!experience || experience.length === 0) return null;

    return (
        <section className="py-20 px-4 bg-slate-50 dark:bg-slate-800">
            <div className="max-w-6xl mx-auto">
                <h2 className="text-4xl font-bold text-slate-900 dark:text-white mb-12 text-center">
                    Work Experience
                </h2>

                <div className="space-y-8">
                    {experience.map((exp, index) => (
                        <div
                            key={exp.id}
                            className="group relative bg-white dark:bg-slate-900 rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-slate-200 dark:border-slate-700"
                            style={{ animationDelay: `${index * 100}ms` }}
                        >
                            {/* Timeline dot */}
                            <div className="absolute -left-4 top-8 w-8 h-8 bg-indigo-600 rounded-full border-4 border-slate-50 dark:border-slate-800 shadow-lg hidden md:block"></div>

                            <div className="flex flex-col md:flex-row gap-6">
                                {/* Logo */}
                                {exp.logo && (
                                    <div className="flex-shrink-0">
                                        <img
                                            src={resolveMediaUrl(exp.logo)}
                                            alt={exp.company}
                                            className="w-20 h-20 rounded-lg object-cover border-2 border-slate-200 dark:border-slate-700"
                                        />
                                    </div>
                                )}

                                {/* Content */}
                                <div className="flex-1">
                                    <div className="flex flex-col md:flex-row md:items-start md:justify-between mb-4">
                                        <div>
                                            <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-1">
                                                {exp.position}
                                            </h3>
                                            <p className="text-lg font-semibold text-indigo-600 dark:text-indigo-400 flex items-center gap-2 mb-2">
                                                <Building size={20} />
                                                {exp.company}
                                            </p>
                                            {exp.employment_type && (
                                                <span className="inline-block px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 text-xs font-semibold rounded-full">
                                                    {exp.employment_type}
                                                </span>
                                            )}
                                        </div>
                                        <div className="mt-2 md:mt-0 text-left md:text-right">
                                            <p className="text-sm text-slate-600 dark:text-slate-400 flex items-center gap-1">
                                                <Calendar size={16} />
                                                {exp.start_month_year} - {exp.end_month_year || 'Present'}
                                            </p>
                                            {exp.location && (
                                                <p className="text-sm text-slate-600 dark:text-slate-400 flex items-center gap-1 mt-1">
                                                    <MapPin size={16} />
                                                    {exp.location}
                                                </p>
                                            )}
                                        </div>
                                    </div>

                                    {exp.description && (
                                        <div className="text-slate-600 dark:text-slate-400 leading-relaxed">
                                            <p className="whitespace-pre-line">{exp.description}</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default ExperienceSection;
