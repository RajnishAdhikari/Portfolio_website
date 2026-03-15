import React from 'react';
import { GraduationCap, MapPin, Calendar } from 'lucide-react';
import { resolveMediaUrl } from '@/lib/media';

const EducationSection = ({ education }) => {
    if (!education || education.length === 0) return null;

    return (
        <section className="py-20 px-4 bg-white dark:bg-slate-900">
            <div className="max-w-6xl mx-auto">
                <h2 className="text-4xl font-bold text-slate-900 dark:text-white mb-12 text-center">
                    Education
                </h2>

                <div className="space-y-8">
                    {education.map((edu, index) => (
                        <div
                            key={edu.id}
                            className="group relative bg-gradient-to-br from-white to-slate-50 dark:from-slate-800 dark:to-slate-900 rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-slate-200 dark:border-slate-700"
                            style={{ animationDelay: `${index * 100}ms` }}
                        >
                            {/* Timeline dot */}
                            <div className="absolute -left-4 top-8 w-8 h-8 bg-blue-600 rounded-full border-4 border-white dark:border-slate-900 shadow-lg hidden md:block"></div>

                            <div className="flex flex-col md:flex-row gap-6">
                                {/* Logo */}
                                {edu.logo && (
                                    <div className="flex-shrink-0">
                                        <img
                                            src={resolveMediaUrl(edu.logo)}
                                            alt={edu.institution}
                                            className="w-20 h-20 rounded-lg object-cover border-2 border-slate-200 dark:border-slate-700"
                                        />
                                    </div>
                                )}

                                {/* Content */}
                                <div className="flex-1">
                                    <div className="flex flex-col md:flex-row md:items-start md:justify-between mb-4">
                                        <div>
                                            <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-1">
                                                {edu.degree}
                                            </h3>
                                            {edu.field && (
                                                <p className="text-lg text-blue-600 dark:text-blue-400 mb-2">
                                                    {edu.field}
                                                </p>
                                            )}
                                            <p className="text-lg font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-2">
                                                <GraduationCap size={20} />
                                                {edu.institution}
                                            </p>
                                        </div>
                                        <div className="mt-2 md:mt-0 text-left md:text-right">
                                            {edu.grade && (
                                                <p className="text-sm font-semibold text-green-600 dark:text-green-400 mb-2">
                                                    {edu.grade}
                                                </p>
                                            )}
                                            <p className="text-sm text-slate-600 dark:text-slate-400 flex items-center gap-1">
                                                <Calendar size={16} />
                                                {edu.start_month_year} - {edu.end_month_year || 'Present'}
                                            </p>
                                            {edu.location && (
                                                <p className="text-sm text-slate-600 dark:text-slate-400 flex items-center gap-1 mt-1">
                                                    <MapPin size={16} />
                                                    {edu.location}
                                                </p>
                                            )}
                                        </div>
                                    </div>

                                    {edu.description && (
                                        <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                                            {edu.description}
                                        </p>
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

export default EducationSection;
