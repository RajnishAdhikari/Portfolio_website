import React from 'react';
import { Code, Layers, Star } from 'lucide-react';

const SkillsSection = ({ skills }) => {
    if (!skills || skills.length === 0) return null;

    // Group skills by category
    const groupedSkills = skills.reduce((acc, skill) => {
        const category = skill.category || 'Other';
        if (!acc[category]) {
            acc[category] = [];
        }
        acc[category].push(skill);
        return acc;
    }, {});

    const categoryIcons = {
        'Programming Languages': Code,
        'Frameworks & Libraries': Layers,
        'Tools & Technologies': Star,
        'Other': Code
    };

    return (
        <section className="py-20 px-4 bg-white dark:bg-slate-900">
            <div className="max-w-6xl mx-auto">
                <h2 className="text-4xl font-bold text-slate-900 dark:text-white mb-12 text-center">
                    Skills & Technologies
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {Object.entries(groupedSkills).map(([category, categorySkills], index) => {
                        const Icon = categoryIcons[category] || Code;
                        return (
                            <div
                                key={category}
                                className="bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-800 dark:to-slate-900 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-slate-200 dark:border-slate-700"
                                style={{ animationDelay: `${index * 100}ms` }}
                            >
                                <div className="flex items-center gap-3 mb-4">
                                    <div className="p-3 bg-blue-600 rounded-lg">
                                        <Icon size={24} className="text-white" />
                                    </div>
                                    <h3 className="text-xl font-bold text-slate-900 dark:text-white">
                                        {category}
                                    </h3>
                                </div>

                                <div className="flex flex-wrap gap-2">
                                    {categorySkills.map((skill) => (
                                        <span
                                            key={skill.id}
                                            className="px-4 py-2 bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg text-sm font-medium shadow-sm hover:shadow-md hover:scale-105 transition-all duration-200 cursor-default border border-slate-200 dark:border-slate-600"
                                            title={skill.proficiency ? `Proficiency: ${skill.proficiency}` : ''}
                                        >
                                            {skill.name}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </section>
    );
};

export default SkillsSection;
