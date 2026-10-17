import { Construction, Droplets, Lightbulb, Trash2, Waves, CircleHelp } from 'lucide-react';
export const CATEGORIES = [
  { value:'roads', label:'Roads & potholes', icon:Construction, color:'orange' },
  { value:'water', label:'Water supply', icon:Droplets, color:'blue' },
  { value:'lighting', label:'Street lighting', icon:Lightbulb, color:'yellow' },
  { value:'waste', label:'Waste collection', icon:Trash2, color:'green' },
  { value:'drainage', label:'Drainage & flooding', icon:Waves, color:'purple' },
  { value:'other', label:'Other service', icon:CircleHelp, color:'slate' },
];
export const STATUS = { pending:{label:'Pending', tone:'pending'}, in_progress:{label:'In progress', tone:'progress'}, resolved:{label:'Resolved', tone:'resolved'} };
export const fmtDate = (d) => d ? new Intl.DateTimeFormat('en-KE',{day:'numeric',month:'short',year:'numeric'}).format(new Date(d)) : '—';
