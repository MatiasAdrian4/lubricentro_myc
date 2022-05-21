/* tslint:disable */
/* eslint-disable */
/**
 * Lubricentro M&C
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * Contact: matiasadrianpp4@gmail.com
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface SalesPerYear
 */
export interface SalesPerYear {
    /**
     * 
     * @type {Array<number>}
     * @memberof SalesPerYear
     */
    salesPerYear?: Array<number>;
}

export function SalesPerYearFromJSON(json: any): SalesPerYear {
    return SalesPerYearFromJSONTyped(json, false);
}

export function SalesPerYearFromJSONTyped(json: any, ignoreDiscriminator: boolean): SalesPerYear {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'salesPerYear': !exists(json, 'sales_per_year') ? undefined : json['sales_per_year'],
    };
}

export function SalesPerYearToJSON(value?: SalesPerYear | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'sales_per_year': value.salesPerYear,
    };
}

