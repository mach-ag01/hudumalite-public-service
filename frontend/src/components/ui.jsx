import React from 'react';
import { ArrowUpRight, Landmark, ClipboardList } from 'lucide-react';
import { CATEGORIES, STATUS } from '../constants';
function Brand({ small=false }) { return <div className={`brand ${small?'brand-small':''}`}><span className="brand-mark"><Landmark size={21}/></span><span>huduma<span className="brand-lite">lite</span><small>PUBLIC SERVICE PORTAL</small></span></div>; }
function StatusPill({ status }) { const s=STATUS[status]||STATUS.pending; return <span className={`status-pill ${s.tone}`}><i/>{s.label}</span>; }
function CategoryIcon({ category, size=18 }) { const item=CATEGORIES.find(c=>c.value===category)||CATEGORIES[5]; const Icon=item.icon; return <span className={`category-icon ${item.color}`}><Icon size={size}/></span>; }
function StatCard({ title, value, note, icon:Icon, tone='green', trend }) { return <div className="stat-card"><div className={`stat-icon ${tone}`}><Icon size={20}/></div><div className="stat-label">{title}</div><div className="stat-value">{value}</div><div className="stat-foot">{trend && <span className="trend"><ArrowUpRight size={13}/>{trend}</span>}<span>{note}</span></div></div>; }
function EmptyState({title,text}) { return <div className="empty-state"><span><ClipboardList size={25}/></span><h3>{title}</h3><p>{text}</p></div>; }
export { Brand, StatusPill, CategoryIcon, StatCard, EmptyState };
