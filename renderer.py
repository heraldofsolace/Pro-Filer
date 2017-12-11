from PEng.engine import DefaultEngine
from PEng.context import Context
from infogatherer import Info
from PEng.template import Template
import plotly.offline as py
import plotly.graph_objs as go


class Renderer:
    def __init__(self,info,options = None):
        if not isinstance(info,Info):
            raise Exception # TODO: Needs info class
        self.info = info
        self.options = options
        self.engine = DefaultEngine()
        self.engine.templates_path = './templates'

    def _prepare_data(self):
        path =self.info.path
        file_list = self.info.file_list
        folder_list = self.info.folder_list
        f_extension_list = self.info.f_extension_list
        f_extension_size_list = self.info.f_extension_size_list
        f_type_list = self.info.f_type_list
        f_type_size_list = self.info.f_type_size_list
        folder_count = self.info.folder_count
        file_count = self.info.file_count
        invoke_time = self.info.invoke_time

        folder_list_sorted_on_size = sorted(folder_list,key=lambda x:x[1][0],reverse=True)
        folder_list_sorted_on_file_count = sorted(folder_list,key=lambda x:x[1][1],reverse=True)
        # print(folder_list_sorted_on_size)
        file_list_sorted_on_size = sorted(file_list,key=lambda x:x[1],reverse=True)
        t_ext_list = []
        for ext,count in f_extension_size_list.items():
            t_ext_list.append((ext,count))
        t_ext_list.sort(key=lambda x:x[1],reverse=True)
        f_extension_list_sorted_on_count = list(t_ext_list)
        t_ext_list = []
        for ext,f in f_extension_list.items():
            t_ext_list.append((ext,sum([x[1] for x in f])))
        t_ext_list.sort(key=lambda x:x[1],reverse=True)
        f_extension_list_sorted_on_size = list(t_ext_list)
        t_ext_list = []
        for type,count in f_type_size_list.items():
            t_ext_list.append((type,count))
        t_ext_list.sort(key=lambda x:x[1],reverse=True)
        f_type_list_sorted_on_count = list(t_ext_list)
        t_ext_list = []
        for type,f in f_type_list.items():
            t_ext_list.append((type,sum(x[1] for x in f)))
        t_ext_list.sort(key=lambda x:x[1],reverse=True)
        f_type_list_sorted_on_size = list(t_ext_list)


        ctx = {
            'path':path,
            'invoke_time_time':invoke_time.time(),
            'invoke_time_date':invoke_time.date(),
            'time_taken':self.info.time_taken,
            'file_count':file_count,
            'folder_count':folder_count,
            'folder_size_count': sum([i[1][0] for i in folder_list_sorted_on_size]),
            'folder_list':folder_list,
            'folder_list_file_count_top_20':folder_list_sorted_on_file_count[:20],
            'folder_list_size_top_20':folder_list_sorted_on_size[:20],
            'folder_list_file_count_last_20':folder_list_sorted_on_file_count[-20:],
            'folder_list_size_last_20':folder_list_sorted_on_size[-20:],
            'file_list': file_list,
            'file_list_top_20':file_list_sorted_on_size[:20],
            'file_list_last_20':file_list_sorted_on_size[-20:],
            'f_extension_list':f_extension_list,
            'f_extension_list_sorted_on_count':f_extension_list_sorted_on_count,
            'f_extension_list_sorted_on_size':f_extension_list_sorted_on_size,
            'f_extension_list_count_top_20':f_extension_list_sorted_on_count[:20],
            'f_extension_list_size_top_20':f_extension_list_sorted_on_size[:20],
            'f_extension_list_count_last_20':f_extension_list_sorted_on_count[-20:],
            'f_extension_list_size_last_20':f_extension_list_sorted_on_size[-20:],
            'f_type_list': f_type_list,
            'f_type_list_sorted_on_count': f_type_list_sorted_on_count,
            'f_type_list_sorted_on_size': f_type_list_sorted_on_size,
            'f_type_list_count_top_20': f_type_list_sorted_on_count[:20],
            'f_type_list_size_top_20': f_type_list_sorted_on_size[:20],
            'f_type_list_count_last_20': f_type_list_sorted_on_count[-20:],
            'f_type_list_size_last_20': f_type_list_sorted_on_size[-20:],
            'top_10_extensions_count':[i[0] for i in f_extension_list_sorted_on_count][:10],
            'top_10_extensions_size':[i[0] for i in f_extension_list_sorted_on_size][:10],
            'top_10_types_count':[i[0] for i in f_type_list_sorted_on_count][:10],
            'top_10_types_size':[i[0] for i in f_type_list_sorted_on_size][:10],


        }
        return ctx

    def render(self,out):
        ctx = self._prepare_data()
        plot_file_list = go.Bar(x=[file[0] for file in ctx['file_list']],y=[file[1] for file in ctx['file_list']])

        plot_folder_list_on_size = go.Bar(
            x=[folder[0] for folder in ctx['folder_list']],
            y=[folder[1][0] for folder in ctx['folder_list']]
        )
        plot_folder_list_on_count = go.Bar(
            x=[folder[0] for folder in ctx['folder_list']],
            y=[folder[1][1] for folder in ctx['folder_list']]
        )

        plot_file_top_20 = go.Bar(
            x=[file[0] for file in ctx['file_list_top_20']],
            y=[file[1] for file in ctx['file_list_top_20']]
        )
        plot_file_last_20 = go.Bar(
            x=[file[0] for file in ctx['file_list_last_20']],
            y=[file[1] for file in ctx['file_list_last_20']]
        )

        plot_extension_list_on_count = go.Bar(
            x=[extn[0] for extn in ctx['f_extension_list_sorted_on_count']],
            y=[extn[1] for extn in ctx['f_extension_list_sorted_on_count']]
        )

        plot_extension_list_on_size = go.Bar(
            x=[extn[0] for extn in ctx['f_extension_list_sorted_on_size']],
            y=[extn[1] for extn in ctx['f_extension_list_sorted_on_size']]
        )

        plot_extension_list_count_top_20 = go.Bar(
            x=[extn[0] for extn in ctx['f_extension_list_count_top_20']],
            y=[extn[1] for extn in ctx['f_extension_list_count_top_20']]
        )
        plot_extension_list_count_last_20 = go.Bar(
            x=[extn[0] for extn in ctx['f_extension_list_count_last_20']],
            y=[extn[1] for extn in ctx['f_extension_list_count_last_20']]
        )
        plot_extension_list_size_top_20 = go.Bar(
            x=[extn[0] for extn in ctx['f_extension_list_size_top_20']],
            y=[extn[1] for extn in ctx['f_extension_list_size_last_20']]
        )
        plot_extension_list_size_last_20 = go.Bar(
            x=[extn[0] for extn in ctx['f_extension_list_size_last_20']],
            y=[extn[1] for extn in ctx['f_extension_list_size_last_20']]
        )

        plot_type_list_on_count = go.Bar(
            x=[type[0] for type in ctx['f_type_list_sorted_on_count']],
            y=[type[1] for type in ctx['f_type_list_sorted_on_count']]
        )
        plot_type_list_count_top_20 = go.Bar(
            x=[type[0] for type in ctx['f_type_list_count_top_20']],
            y=[type[1] for type in ctx['f_type_list_count_top_20']]
        )
        plot_type_list_count_last_20 = go.Bar(
            x=[type[0] for type in ctx['f_type_list_count_last_20']],
            y=[type[1] for type in ctx['f_type_list_count_last_20']]
        )
        plot_type_list_on_size = go.Bar(
            x=[type[0] for type in ctx['f_type_list_sorted_on_size']],
            y=[type[1] for type in ctx['f_type_list_sorted_on_size']]
        )
        plot_type_list_size_top_20 = go.Bar(
            x=[type[0] for type in ctx['f_type_list_size_top_20']],
            y=[type[1] for type in ctx['f_type_list_size_top_20']]
        )
        plot_type_list_size_last_20 = go.Bar(
            x=[type[0] for type in ctx['f_type_list_size_last_20']],
            y=[type[1] for type in ctx['f_type_list_size_last_20']]
        )

        plotted_folder_list_on_size = py.plot([plot_folder_list_on_size],output_type='div',include_plotlyjs=False)
        plotted_folder_list_on_count = py.plot([plot_folder_list_on_count],output_type='div',include_plotlyjs=False)
        plotted_file_top_20 = py.plot([plot_file_top_20],output_type='div',include_plotlyjs=False)
        plotted_file_last_20 = py.plot([plot_file_last_20],output_type='div',include_plotlyjs=False)
        plotted_file_list = py.plot([plot_file_list],output_type='div',include_plotlyjs=False)
        plotted_extension_list_on_size = py.plot([plot_extension_list_on_size],output_type='div',include_plotlyjs=False)
        plotted_extension_list_on_count = py.plot([plot_extension_list_on_count],output_type='div',include_plotlyjs=False)
        plotted_extension_list_count_top_20 = py.plot([plot_extension_list_count_top_20],output_type='div',include_plotlyjs=False)
        plotted_extension_list_count_last_20 = py.plot([plot_extension_list_count_last_20],output_type='div',include_plotlyjs=False)
        plotted_extension_list_size_top_20 = py.plot([plot_extension_list_size_top_20],output_type='div',include_plotlyjs=False)
        plotted_extension_list_size_last_20 = py.plot([plot_extension_list_size_last_20],output_type='div',include_plotlyjs=False)
        plotted_type_list_on_size = py.plot([plot_type_list_on_size],output_type='div',include_plotlyjs=False)
        plotted_type_list_on_count = py.plot([plot_type_list_on_count],output_type='div',include_plotlyjs=False)
        plotted_type_list_count_top_20 = py.plot([plot_type_list_count_top_20],output_type='div',include_plotlyjs=False)
        plotted_type_list_count_last_20 = py.plot([plot_type_list_count_last_20],output_type='div',include_plotlyjs=False)
        plotted_type_list_size_top_20 = py.plot([plot_type_list_size_top_20],output_type='div',include_plotlyjs=False)
        plotted_type_list_size_last_20 = py.plot([plot_type_list_size_last_20],output_type='div',include_plotlyjs=False)

        grahs = {'plotted_folder_list_on_size':plotted_folder_list_on_size,
                 'plotted_folder_list_on_count':plotted_folder_list_on_count,
                 'plotted_file_top_20':plotted_file_top_20,
                 'plotted_file_last_20':plotted_file_last_20,
                 'plotted_file_list':plotted_file_list,
                 'plotted_extension_list_on_size':plotted_extension_list_on_size,
                 'plotted_extension_list_on_count':plotted_extension_list_on_count,
                 'plotted_extension_list_count_top_20':plotted_extension_list_count_top_20,
                 'plotted_extension_list_count_last_20':plotted_extension_list_count_last_20,
                 'plotted_extension_list_size_top_20':plotted_extension_list_size_top_20,
                 'plotted_extension_list_size_last_20':plotted_extension_list_size_last_20,
                 'plotted_type_list_on_size':plotted_type_list_on_size,
                 'plotted_type_list_on_count':plotted_type_list_on_count,
                 'plotted_type_list_count_top_20':plotted_type_list_count_top_20,
                 'plotted_type_list_count_last_20':plotted_type_list_count_last_20,
                 'plotted_type_list_size_top_20':plotted_type_list_size_top_20,
                 'plotted_type_list_size_last_20':plotted_type_list_size_last_20
                    }
        ctx = Context(self.engine,ctx,'root')
        ctx.push_permanent(grahs,'root')
        # print(ctx['path'])
        t = Template( self.engine.load_template('info_page'))
        with open(out,'w') as f:
            f.write(t.render(ctx))
        # print(t.render(ctx))


if __name__ == '__main__':
    r = Renderer()