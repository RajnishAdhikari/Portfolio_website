import React from 'react';
import { Mail, Phone, MapPin, Send } from 'lucide-react';

const Footer = ({ personalInfo }) => {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="bg-slate-900 dark:bg-black text-white py-12 px-4">
            <div className="max-w-6xl mx-auto">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
                    {/* About */}
                    <div>
                        <h3 className="text-2xl font-bold mb-4">{personalInfo?.full_name || 'Portfolio'}</h3>
                        <p className="text-slate-400">
                            {personalInfo?.tagline || 'Building amazing experiences'}
                        </p>
                    </div>

                    {/* Contact Info */}
                    {personalInfo && (
                        <div>
                            <h4 className="text-lg font-semibold mb-4">Contact</h4>
                            <div className="space-y-2">
                                {personalInfo.email && (
                                    <a
                                        href={`mailto:${personalInfo.email}`}
                                        className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors"
                                    >
                                        <Mail size={16} />
                                        {personalInfo.email}
                                    </a>
                                )}
                                {personalInfo.phone && (
                                    <div className="flex items-center gap-2 text-slate-400">
                                        <Phone size={16} />
                                        {personalInfo.phone}
                                    </div>
                                )}
                                {personalInfo.address && (
                                    <div className="flex items-center gap-2 text-slate-400">
                                        <MapPin size={16} />
                                        {personalInfo.address}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Quick Links */}
                    <div>
                        <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
                        <div className="space-y-2">
                            <a href="#about" className="block text-slate-400 hover:text-white transition-colors">
                                About
                            </a>
                            <a href="#experience" className="block text-slate-400 hover:text-white transition-colors">
                                Experience
                            </a>
                            <a href="#projects" className="block text-slate-400 hover:text-white transition-colors">
                                Projects
                            </a>
                            <a href="/admin/login" className="block text-slate-400 hover:text-white transition-colors">
                                Admin Login
                            </a>
                        </div>
                    </div>
                </div>

                <div className="border-t border-slate-800 pt-8 text-center">
                    <p className="text-slate-400">
                        © {currentYear} {personalInfo?.full_name || 'Portfolio'}. All rights reserved.
                    </p>
                    <p className="text-slate-500 text-sm mt-2">
                        Built with React & FastAPI
                    </p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
