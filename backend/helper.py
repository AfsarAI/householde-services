import base64
from datetime import datetime
import io
from flask import logging, session
import logging
from matplotlib import cm, pyplot as plt
import matplotlib
from matplotlib.patches import Patch, Rectangle
matplotlib.use('Agg')  




from sqlalchemy.engine.row import Row
from datetime import datetime

def format_dates(query_results, date_fields=None):
    """
    Formats date fields for a list of query results or a single result.

    :param query_results: List of model instances, single instance, or Row objects.
    :param date_fields: List of date field names to format (e.g., ['date', 'date_of_request']).
    :return: Query results with formatted date fields, maintaining the original type.
    """
    if not query_results:
        return query_results

    date_fields = date_fields or []

    
    is_single = not isinstance(query_results, list)
    if is_single:
        query_results = [query_results]  

    formatted_results = []

    for result in query_results:
        if isinstance(result, Row):
            
            result_dict = dict(result._mapping)  
            for field in date_fields:
                if field in result_dict:
                    date_value = result_dict[field]
                    result_dict[f"formatted_{field}"] = (
                        date_value.strftime('%d-%m-%Y %I:%M %p') if date_value and isinstance(date_value, datetime) else "N/A"
                    )
            formatted_results.append(result_dict)
        else:
            
            for field in date_fields:
                date_value = getattr(result, field, None)
                setattr(
                    result,
                    f"formatted_{field}",
                    date_value.strftime('%d-%m-%Y %I:%M %p') if date_value and isinstance(date_value, datetime) else "N/A"
                )
            formatted_results.append(result)

    
    return formatted_results[0] if is_single else formatted_results





logging.basicConfig(level=logging.DEBUG)


def set_session(id, email, role):
    if 'sessions' not in session:
        session['sessions'] = {}

    session_key = f"{role}_{id}"
    session['sessions'][session_key] = {"id":id, "email": email, "role": role}
    session[f"{role}_email"] = email  
    session[f"{role}_id"] = id  
    session['role'] = role  
    session.permanent = True  
    logging.debug(f"Session set for {role}: {session_key}")






def generate_pie_chart(data, title):
    """Utility function to generate a pie chart with labels and matching colors"""
    labels = list(data.keys())
    sizes = list(data.values())

    
    if sum(sizes) == 0:
        return None  

    fig = plt.figure(figsize=(10, 10))  
    fig.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.15)

    
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,  
        autopct=lambda p: '{:.0f}'.format(p * sum(sizes) / 100) if p > 0 else '',  
        startangle=140,
        textprops={'fontsize': 10},  
        wedgeprops={'edgecolor': 'black', 'linewidth': 2}
    )

    
    plt.title(
        title, pad=30, fontsize=20, loc='right', fontweight='bold', color='blue'
    )

    
    for autotext, wedge in zip(autotexts, wedges):
        autotext.set_color('white')  
        autotext.set_fontsize(15)  
        autotext.set_bbox(
            dict(facecolor=wedge.get_facecolor(), alpha=0.6, edgecolor='none')
        )  

    
    for text, wedge in zip(texts, wedges):
        text.set_color(wedge.get_facecolor())  
        text.set_fontsize(20)  
        text.set_fontweight('bold')  

    
    legend = plt.legend(
        wedges,
        labels,  
        loc='upper left',
        bbox_to_anchor=(1.01, 1),
        fontsize=35,
        borderaxespad=0.6,  
        title="Service Status",
        prop={'weight': 'bold'},  
        handleheight=1.5,  
        handlelength=3,  
        labelspacing=1  
    )
    legend.get_title().set_fontsize(13)  
    legend.get_title().set_fontweight('bold')  

    
    for legend_text, wedge in zip(legend.get_texts(), wedges):
        legend_text.set_color(wedge.get_facecolor())  

    
    ax = plt.gca()  
    ax.add_patch(
        Rectangle(
            (0, 0), 1, 1,  
            transform=ax.transAxes,  
            edgecolor="black",
            linewidth=4,
            fill=False,  
        )
    )

    
    plt.tight_layout()

    
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    chart_data = base64.b64encode(img.getvalue()).decode("utf-8")
    plt.close()

    return chart_data



def generate_vertical_bar_chart(data, title, xlabel="Status", cmap='viridis'):
    """Utility function to generate a vertical bar chart"""
    labels = list(data.keys())
    sizes = list(data.values())
    
    
    color_map = cm.get_cmap(cmap, len(labels))
    colors = [color_map(i) for i in range(len(labels))]

    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, sizes, color=colors, edgecolor='black')

    
    plt.title(title, pad=20, fontsize=20, fontweight='bold', color='blue')  
    plt.xlabel(xlabel, labelpad=15, fontsize=16, fontweight='bold', color='green')  
    plt.ylabel("Count", labelpad=15, fontsize=16, fontweight='bold', color='green')  
    plt.grid(axis='y', linestyle='--', alpha=0.21)  

    
    patches = [Patch(color=color, label=label) for color, label in zip(colors, labels)]

    
    for bar, color in zip(bars, colors):
        height = bar.get_height()
        plt.annotate(
            f"{height}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),  
            textcoords="offset points",
            ha='center', va='bottom',
            color=color,  
            fontsize=12,
            fontweight='bold'
        )

    
    legend = plt.legend(handles=patches, loc='upper right', bbox_to_anchor=(1.35, 1), prop={'weight': 'bold'})

    
    for text, color in zip(legend.get_texts(), colors):
        text.set_color(color)

    
    plt.tight_layout()

    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_data = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return chart_data



def generate_horizontal_bar_chart(data, title, ylabel="Status", cmap='viridis'):
    """Utility function to generate a horizontal bar chart"""
    labels = list(data.keys())
    sizes = list(data.values())
    
    
    color_map = cm.get_cmap(cmap, len(labels))
    colors = [color_map(i) for i in range(len(labels))]

    
    fig = plt.figure(figsize=(10, 8))
    fig.subplots_adjust(
        left=0.15, 
        right=0.85, 
        top=0.85, 
        bottom=0.15
    )
    bars = plt.barh(labels, sizes, color=colors, edgecolor='black')  

    
    plt.title(
        title, 
        pad=30,  
        fontsize=23,  
        fontweight='bold',
        loc='center',  
        color='blue'
    )
    plt.xlabel("Count", labelpad=15, fontsize=20, fontweight='bold', color='green')  
    plt.ylabel(ylabel, labelpad=15, fontsize=20, fontweight='bold', color='green')  
    plt.grid(axis='x', linestyle='--', alpha=0.21)  

    
    patches = [Patch(color=color, label=label) for color, label in zip(colors, labels)]
    legend = plt.legend(handles=patches, loc='upper right', bbox_to_anchor=(1.3, 1), prop={'weight': 'bold'})

    
    for text, color in zip(legend.get_texts(), colors):
        text.set_color(color)

    
    for bar, color in zip(bars, colors):
        width = bar.get_width()
        plt.annotate(
            f"{width}",
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(5, 0),  
            textcoords="offset points",
            ha='left', va='center',
            color=color,  
            fontsize=12,
            fontweight='bold'
        )
        
    
    plt.tight_layout()

    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_data = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return chart_data
